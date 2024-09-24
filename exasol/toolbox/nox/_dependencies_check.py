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
    dependencies = Dependencies(content).parse()
    console = rich.console.Console()
    illegal = dependencies.illegal()
    report_illegal(illegal, console)
    if illegal:
        sys.exit(1)


class Dependencies:
    ILLEGAL_DEPENDENCIES = ['url', 'git', 'path']

    def __init__(self, pyproject_toml: str):
        self.illegal_dict: Dict[str, List[str]] = {}
        self.content = pyproject_toml

    def parse(self) -> "Dependencies":
        def source_filter(version) -> bool:
            for f in self.ILLEGAL_DEPENDENCIES:
                if f in version:
                    return True
            return False

        def extract_dependencies(section) -> List[str]:
            dependencies = []
            for name, version in section.items():
                if source_filter(version):
                    dependencies.append(f"{name} = {version}")
            return dependencies

        illegal: Dict[str, List[str]] = {}
        toml = tomlkit.loads(self.content)
        poetry = toml.get("tool", {}).get("poetry", {})

        part = poetry.get("dependencies", {})
        dependencies_list = extract_dependencies(part)
        if dependencies_list:
            illegal["tool.poetry.dependencies"] = dependencies_list

        part = poetry.get("dev", {}).get("dependencies", {})
        dependencies_list = extract_dependencies(part)
        if dependencies_list:
            illegal["tool.poetry.dev.dependencies"] = dependencies_list

        part = poetry.get("group", {})
        for group, content in part.items():
            dependencies_list = extract_dependencies(content.get("dependencies", {}))
            if dependencies_list:
                illegal[f"tool.poetry.group.{group}.dependencies"] = dependencies_list

        self.illegal_dict = illegal
        return self

    def illegal(self) -> Dict[str, List[str]]:
        return self.illegal_dict


def report_illegal(illegal: Dict[str, List[str]], console: rich.console.Console):
    if illegal:
        count = sum(len(deps) for deps in illegal.values())
        suffix = "y" if count == 1 else "ies"
        console.print(f"{count} illegal dependenc{suffix}\n", style="red")
        for section, dependencies in illegal.items():
            console.print(f"\\[{section}]", style="red")
            for dependency in dependencies:
                console.print(dependency, style="red")
            console.print("")
    else:
        console.print("Success: All dependencies refer to explicit pipy releases.", style="green")
