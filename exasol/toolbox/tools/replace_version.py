from pathlib import Path
from typing import List


def update_workflow(template: Path, version: str) -> None:
    """Updates versions of XYZ in GitHub workflow ..."""
    with open(template, encoding="utf-8") as file:
        content = file.readlines()

    content = update_versions(
        lines=content, matcher="exasol/python-toolbox/.github/", version=version
    )

    with open(template, "w", encoding="utf-8") as file:
        file.writelines(content)


def is_update_required(line, matcher):
    return matcher in line and "@" in line


def update_version(line, version):
    keep = line[: line.index("@") + 1]
    updated = f"{version}\n"
    return f"{keep}{updated}"


def update_versions(lines, matcher, version) -> List[str]:
    result = []
    for line in lines:
        if is_update_required(line, matcher):
            line = update_version(line, version)
        result.append(line)
    return result
