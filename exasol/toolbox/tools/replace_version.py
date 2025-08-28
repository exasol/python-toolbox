import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import (
    Callable,
    Optional,
)

from exasol.toolbox.util.version import Version


def update_github_yml(template: Path, version: Version) -> None:
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
    version_pattern: str

    @property
    def full_pattern(self) -> str:
        return f"{self.match_pattern}{self.break_pattern}{self.version_pattern}"

    def replace_version(self, line: str, version: str) -> str:
        return re.sub(
            f"{self.break_pattern}{self.version_pattern}",
            f"{self.break_pattern}{version}",
            line,
        )


def full_version_modifier(version: Version) -> str:
    return str(version)


def major_version_modifier(version: Version) -> str:
    return f"v{version.major}"


class GithubActionsReplacement:
    def __init__(
        self, pattern: Pattern, version_string_modifier: Callable[[Version], str]
    ) -> None:
        self.pattern = pattern
        self.version_string_modifier = version_string_modifier

    def replace_version(self, line: str, version: Version) -> Optional[str]:
        match = re.search(self.pattern.full_pattern, line)
        if match:
            return self.pattern.replace_version(
                line=line, version=self.version_string_modifier(version)
            )
        return None


class Replacements(Enum):
    github = GithubActionsReplacement(
        pattern=Pattern(
            match_pattern="exasol/python-toolbox/.github/[^/]+/[^/]+",
            break_pattern="@",
            version_pattern=r"v[0-9]+",
        ),
        version_string_modifier=major_version_modifier,
    )

    pypi = GithubActionsReplacement(
        pattern=Pattern(
            match_pattern="exasol-toolbox",
            break_pattern="==",
            version_pattern=r"[0-9]+\.[0-9]+\.[0-9]+",
        ),
        version_string_modifier=full_version_modifier,
    )


def _update_line_with_version(line: str, version: Version) -> str:
    for replacement in Replacements:
        if replaced_line := replacement.value.replace_version(
            line=line, version=version
        ):
            return replaced_line
    return line


def update_versions(lines: list[str], version: Version) -> list[str]:
    return [_update_line_with_version(line=line, version=version) for line in lines]
