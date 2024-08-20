from tomlkit import loads
from sys import exit
import pytest


FILTER = ['url', 'git', 'path']


def _source_filter(version, filter):
    output = False
    if isinstance(version, dict):
        for key in version.keys():
            if key in filter:
                output = True
    return output


def dependency_check():
    with open("pyproject.toml", 'r') as toml:
        toml = loads(toml.read())
    for _, version in toml["tool"]["poetry"]["dependencies"].items():
        if _source_filter(version, FILTER):
            exit(1)
            pass
    exit(0)


if __name__ == "__main__":
    dependency_check()
