from __future__ import annotations

from typing import (
    Iterable,
    List,
    Dict
)

import nox
from nox import Session

from exasol.toolbox.nox._shared import python_files
from noxconfig import PROJECT_CONFIG

from pathlib import Path
import rich.console
import tomlkit
import sys


def _pylint(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "pylint",
        "--output-format",
        "colorized,json:.lint.json,text:.lint.txt",
        *files,
    )


def _type_check(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
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
        "poetry",
        "run",
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--format",
        "json",
        "--output",
        ".security.json",
        "--exit-zero",
        *files,
    )
    session.run(
        "poetry",
        "run",
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--exit-zero",
        *files,
    )


class Dependencies:
    def __init__(self, illegal: Dict[str, List[str]] | None):
        self._illegal = illegal or {}

    @staticmethod
    def parse(pyproject_toml: str) -> "Dependencies":
        def _source_filter(version) -> bool:
            ILLEGAL_SPECIFIERS = ['url', 'git', 'path']
            return any(
                specifier in version
                for specifier in ILLEGAL_SPECIFIERS
            )

        def find_illegal(part) -> List[str]:
            return [
                f"{name} = {version}"
                for name, version in part.items()
                if _source_filter(version)
            ]

        illegal: Dict[str, List[str]] = {}
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
    def illegal(self) -> Dict[str, List[str]]:
        return self._illegal


def report_illegal(illegal: Dict[str, List[str]], console: rich.console.Console):
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
    "Runs the static code analyzer on the project"
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _pylint(session, py_files)


@nox.session(name="lint:typing", python=False)
def type_check(session: Session) -> None:
    """Runs the type checker on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _type_check(session, py_files)


@nox.session(name="lint:security", python=False)
def security_lint(session: Session) -> None:
    """Runs the security linter on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _security_lint(session, list(filter(lambda file: "test" not in file, py_files)))


@nox.session(name="lint:dependencies", python=False)
def dependency_check(session: Session) -> None:
    """Checks if only valid sources of dependencies are used"""
    content = Path(PROJECT_CONFIG.root, "pyproject.toml").read_text()
    dependencies = Dependencies.parse(content)
    console = rich.console.Console()
    if illegal := dependencies.illegal:
        report_illegal(illegal, console)
        sys.exit(1)