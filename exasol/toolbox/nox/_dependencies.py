from __future__ import annotations
import tomlkit
import sys
from pathlib import Path
import nox
from nox import Session
from noxconfig import PROJECT_CONFIG
from typing import (
    List,
    Dict
)
import rich.console


@nox.session(name="dependencies-check", python=False)
def dependency_check(session: Session) -> None:
    content = Path(PROJECT_CONFIG.root, "pyproject.toml").read_text()
    dependencies = Dependencies.parse(content)
    console = rich.console.Console()
    if illegal := dependencies.illegal:
        report_illegal(illegal, console)
        sys.exit(1)


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
