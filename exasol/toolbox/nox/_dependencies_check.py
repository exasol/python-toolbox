import tomlkit
import sys
from pathlib import Path
import nox
from nox import Session
from noxconfig import PROJECT_CONFIG


FILTERS = ['url', 'git', 'path']


@nox.session(name="dependencies-check", python=False)
def dependency_check(session: Session) -> None:
    file = Path(PROJECT_CONFIG.root, "pyproject.toml")
    output = _dependencies_check(file.read_text())
    print("\033[31m"+output) if output else print("\033[32m"+"Success: no wrong dependencies found")
    sys.exit(0 if not output else 1)


def _source_filter(version, filters) -> bool:
    for f in filters:
        if f in version:
            return True
    return False


def extract_dependencies(section, filters) -> list[str]:
    dependencies = []
    for name, version in section.items():
        if _source_filter(version, filters):
            dependencies.append(f"{name} = {version}")
    return dependencies


def _dependencies_check(string: str) -> str:
    toml = tomlkit.loads(string)
    group_dependencies = {}

    poetry = toml.get("tool", {}).get("poetry", {})

    dependencies = extract_dependencies(poetry.get("dependencies", {}), FILTERS)

    dev_section = poetry.get("dev", {}).get("dependencies", {})
    dev_dependencies = extract_dependencies(dev_section, FILTERS)

    group_section = poetry.get("group", {})
    for group, content in group_section.items():
        group_deps = extract_dependencies(content.get("dependencies", {}), FILTERS)
        if group_deps:
            group_key = f'[tool.poetry.group.{group}.dependencies]'
            group_dependencies[group_key] = group_deps

    total_count = len(dependencies) + len(dev_dependencies) + sum(len(deps) for deps in group_dependencies.values())
    if total_count > 0:
        suffix = "y" if total_count == 1 else "ies"
        output = [f"{total_count} illegal dependenc{suffix}:\n"]

        if dependencies:
            output.append(f"\n[tool.poetry.dependencies]\n" + "\n".join(dependencies) + "\n")
        if dev_dependencies:
            output.append(f"\n[tool.poetry.dev.dependencies]\n" + "\n".join(dev_dependencies) + "\n")
        for key, value in group_dependencies.items():
            output.append(f"\n{key}\n" + "\n".join(value) + "\n")

        return "".join(output)

    return ""


if __name__ == "__main__":
    print(_dependencies_check(Path("pyproject.toml").read_text()))
