from tomlkit import loads
from sys import exit
import pytest


FILTER = ['url', 'git', 'path']


def _source_filter(version, filter):
    output = None
    if isinstance(version, dict):
        for key in version.keys():
            if key in filter:
                output = key
    return output


def dependency_check():
    with open("pyproject.toml", 'r') as toml:
        toml = loads(toml.read())
    dependencies = []
    for name, version in toml["tool"]["poetry"]["dependencies"].items():
        key = _source_filter(version, FILTER)
        if key:
            dependencies.append(f"{name} = {version}")

    if dependencies:
        n = len(dependencies)
        suffix = "y" if n == 1 else "ies"
        output = f"{n} illegal dependenc{suffix}:\n" + "\n".join(dependencies)
        exit(output)


if __name__ == "__main__":
    dependency_check()
