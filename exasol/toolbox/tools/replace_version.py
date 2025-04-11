import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


def update_github_yml(template: Path, version: str) -> None:
    """Updates versions in GitHub workflows and actions"""
    with open(template, encoding="utf-8") as file:
        content = file.readlines()

    content = update_versions(lines=content, version=version)

    with open(template, "w", encoding="utf-8") as file:
        file.writelines(content)


@dataclass(frozen=True)
class Pattern:
    match_pattern: str
    break_pattern: str

    @property
    def version_pattern(self) -> str:
        return r"[0-9]+\.[0-9]+\.[0-9]+"

    @property
    def full_pattern(self) -> str:
        return f"{self.match_pattern}{self.break_pattern}{self.version_pattern}"

    def replace_version(self, line: str, version: str) -> str:
        return re.sub(
            f"{self.break_pattern}{self.version_pattern}",
            f"{self.break_pattern}{version}",
            line,
        )


class ToolboxPattern(Enum):
    github = Pattern(
        match_pattern="exasol/python-toolbox/.github/[^/]+/[^/]+",
        break_pattern="@",
    )
    pypi = Pattern(
        match_pattern="exasol-toolbox",
        break_pattern="==",
    )


def _update_line_with_version(line: str, version: str) -> str:
    for pattern in ToolboxPattern:
        match = re.search(pattern.value.full_pattern, line)
        if match:
            return pattern.value.replace_version(line=line, version=version)
    return line


def update_versions(lines: list[str], version: str) -> list[str]:
    return [_update_line_with_version(line=line, version=version) for line in lines]
