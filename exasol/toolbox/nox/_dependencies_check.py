import tomlkit
import sys
from pathlib import Path
import nox
from nox import Session


FILTERS = ['url', 'git', 'path']


@nox.session(name="dependencies-check", python=False)
def dependency_check(session: Session):
    file = Path("pyproject.toml")
    sys.exit(_dependencies_check(file.read_text()))


def _source_filter(version, filters):
    output = None
    if isinstance(version, dict):
        for key in version.keys():
            if key in filters:
                output = key
    return output


def _dependencies_check(string: str):
    toml = tomlkit.loads(string)
    dependencies: list = []
    dev_dependencies: list = []
    group_dependencies: dict = {}
    if "tool" in toml:
        if "poetry" in toml["tool"].unwrap():
            if "dependencies" in toml["tool"].unwrap()["poetry"]:
                for name, version in toml["tool"].unwrap()["poetry"]["dependencies"].items():
                    key = _source_filter(version, FILTERS)
                    if key:
                        dependencies.append(f"{name} = {version}")

            if "dev" in toml["tool"].unwrap()["poetry"]:
                if "dependencies" in toml["tool"].unwrap()["poetry"]["dev"]:
                    for name, version in toml["tool"].unwrap()["poetry"]["dev"]["dependencies"].items():
                        key = _source_filter(version, FILTERS)
                        if key:
                            dev_dependencies.append(f"{name} = {version}")

            if "group" in toml["tool"].unwrap()["poetry"]:
                for group in toml["tool"].unwrap()["poetry"]["group"]:
                    if "dependencies" in toml["tool"].unwrap()["poetry"]["group"][group]:
                        for name, version in toml["tool"].unwrap()["poetry"]["group"][group]["dependencies"].items():
                            key = _source_filter(version, FILTERS)
                            if key:
                                if f'[tool.poetry.group.{group}.dependencies]' not in group_dependencies:
                                    group_dependencies[f'[tool.poetry.group.{group}.dependencies]'] = []
                                group_dependencies[f'[tool.poetry.group.{group}.dependencies]'].append(f"{name} = {version}")

    if dependencies or dev_dependencies or group_dependencies:
        l = len(dependencies)
        m = len(dev_dependencies)
        n = 0
        for _, dependency in group_dependencies.items():
            n += len(dependency)
        suffix = "y" if l+m+n == 1 else "ies"
        output = f"{l+m+n} illegal dependenc{suffix}:{chr(10)}"
        output += ("\n[tool.poetry.dependencies]\n"+"\n".join(dependencies)+"\n") if l > 0 else ""
        output += ("\n[tool.poetry.dev.dependencies]\n"+"\n".join(dev_dependencies)+"\n") if m > 0 else ""
        output += ("\n".join(f"{chr(10)}{key}{chr(10)}{chr(10).join(value)}"for key, value in group_dependencies.items())) if n > 0 else ""
        output += "\n"
        return output
    return 0
