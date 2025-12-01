from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

import nox
import rich.console
import tomlkit
from nox import Session

from exasol.toolbox.nox._shared import get_filtered_python_files
from exasol.toolbox.util.dependencies.shared_models import PoetryFiles
from noxconfig import PROJECT_CONFIG


def _pylint(session: Session, files: Iterable[str]) -> None:
    json_file = PROJECT_CONFIG.root_path / ".lint.json"
    txt_file = PROJECT_CONFIG.root_path / ".lint.txt"

    session.run(
        "pylint",
        "--output-format",
        f"colorized,json:{json_file},text:{txt_file}",
        *files,
    )


def _type_check(session: Session, files: Iterable[str]) -> None:
    session.run(
        "mypy",
        "--explicit-package-bases",
        "--namespace-packages",
        "--show-error-codes",
        "--pretty",
        "--show-column-numbers",
        "--show-error-context",
        "--scripts-are-modules",
        *files,
    )


def _security_lint(session: Session, files: Iterable[str]) -> None:
    session.run(
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--format",
        "json",
        "--output",
        PROJECT_CONFIG.root_path / ".security.json",
        "--exit-zero",
        *files,
    )
    session.run(
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--exit-zero",
        *files,
    )


def _import_lint(session: Session, path: Path) -> None:
    session.run("lint-imports", "--config", path)


class Dependencies:
    def __init__(self, illegal: dict[str, list[str]] | None):
        self._illegal = illegal or {}

    @staticmethod
    def parse(pyproject_toml: str) -> Dependencies:
        def _source_filter(version) -> bool:
            ILLEGAL_SPECIFIERS = ["url", "git", "path"]
            return any(specifier in version for specifier in ILLEGAL_SPECIFIERS)

        def find_illegal(part) -> list[str]:
            return [
                f"{name} = {version}"
                for name, version in part.items()
                if _source_filter(version)
            ]

        illegal: dict[str, list[str]] = {}
        toml = tomlkit.loads(pyproject_toml)
        poetry = toml.get("tool", {}).get("poetry", {})

        part = poetry.get("dependencies", {})
        if illegal_group := find_illegal(part):
            illegal["tool.poetry.dependencies"] = illegal_group

        part = poetry.get("dev", {}).get("dependencies", {})
        if illegal_group := find_illegal(part):
            illegal["tool.poetry.dev.dependencies"] = illegal_group

        part = poetry.get("group", {})
        for group, content in part.items():
            illegal_group = find_illegal(content.get("dependencies", {}))
            if illegal_group:
                illegal[f"tool.poetry.group.{group}.dependencies"] = illegal_group
        return Dependencies(illegal)

    @property
    def illegal(self) -> dict[str, list[str]]:
        return self._illegal


def report_illegal(illegal: dict[str, list[str]], console: rich.console.Console):
    count = sum(len(deps) for deps in illegal.values())
    suffix = "y" if count == 1 else "ies"
    console.print(f"{count} illegal dependenc{suffix}\n", style="red")
    for section, dependencies in illegal.items():
        console.print(f"\\[{section}]", style="red")
        for dependency in dependencies:
            console.print(dependency, style="red")
        console.print("")


@nox.session(name="lint:code", python=False)
def lint(session: Session) -> None:
    """Runs the static code analyzer on the project"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.source_code_path)
    _pylint(session=session, files=py_files)


@nox.session(name="lint:typing", python=False)
def type_check(session: Session) -> None:
    """Runs the type checker on the project"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.root_path)
    _type_check(session=session, files=py_files)


@nox.session(name="lint:security", python=False)
def security_lint(session: Session) -> None:
    """Runs the security linter on the project"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.source_code_path)
    _security_lint(session=session, files=py_files)


@nox.session(name="lint:dependencies", python=False)
def dependency_check(session: Session) -> None:
    """Checks if only valid sources of dependencies are used"""
    content = Path(PROJECT_CONFIG.root_path, PoetryFiles.pyproject_toml).read_text()
    dependencies = Dependencies.parse(content)
    console = rich.console.Console()
    if illegal := dependencies.illegal:
        report_illegal(illegal, console)
        sys.exit(1)


@nox.session(name="lint:import", python=False)
def import_lint(session: Session) -> None:
    """(experimental) Runs import linter on the project"""
    parser = argparse.ArgumentParser(
        usage="nox -s import-lint -- [options]",
        description="Runs the import linter on the project",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="path to the configuration file for the importlinter",
        metavar="TEXT",
    )

    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    file: str = args.config
    path: Path | None = None
    if file is None:
        path = getattr(
            PROJECT_CONFIG, "import_linter_config", Path(".import_linter_config")
        )
    else:
        path = Path(file)
    if not path.exists():
        session.error(
            "Please make sure you have a configuration file for the importlinter"
        )
    _import_lint(session=session, path=path)
