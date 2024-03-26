from pathlib import Path
from typing import List

def replace_version(template: Path, version: str) -> None:
    with open(template, "r+", encoding="utf8") as file:
        lines = file.readlines()
        _replace(lines, "exasol/python-toolbox/.github/", version)
        file.seek(0)
        file.writelines(lines)


def _replace(lines: List[str], replace_filter: str, version: str) -> None:
    for count, line in enumerate(lines):
        if line.find(replace_filter) != -1:
            if line.find("@") != -1:
                lines[count] = line[0:line.index("@")+1] + version + "\n"
