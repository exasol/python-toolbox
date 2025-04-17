from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import (
    total_ordering,
    wraps,
)
from inspect import cleandoc
from pathlib import Path
from shutil import which

from exasol.toolbox.error import ToolboxError


def _index_or(container, index, default):
    try:
        return container[index]
    except IndexError:
        return default


class ReleaseTypes(Enum):
    Major = "major"
    Minor = "minor"
    Patch = "patch"

    def __str__(self):
        return self.name.lower()


def poetry_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmd = which("poetry")
        if not cmd:
            raise ToolboxError("Couldn't find poetry executable")
        try:
            return func(*args, **kwargs)
        except subprocess.CalledProcessError as ex:
            raise ToolboxError(f"Failed to execute: {ex.cmd}") from ex

    return wrapper


@total_ordering
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: object):
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major < other.major
            or (self.major <= other.major and self.minor < other.minor)
            or (
                self.major <= other.major
                and self.minor <= other.minor
                and self.patch < other.patch
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    @staticmethod
    def from_string(version):
        parts = [int(number, base=0) for number in version.split(".")]
        if len(parts) > 3:
            raise ValueError(
                "Version has an invalid format, "
                f"expected: '<major>.<minor>.<patch>', actual: '{version}'"
            )
        version = [_index_or(parts, i, 0) for i in range(3)]
        return Version(*version)

    @staticmethod
    @poetry_command
    def from_poetry():
        output = subprocess.run(
            ["poetry", "version", "--no-ansi", "--short"],
            capture_output=True,
            text=True,
        )
        return Version.from_string(output.stdout.strip())

    @staticmethod
    @poetry_command
    def upgrade_version_from_poetry(t: ReleaseTypes):
        output = subprocess.run(
            ["poetry", "version", str(t), "--dry-run", "--no-ansi", "--short"],
            capture_output=True,
            text=True,
        )
        return Version.from_string(output.stdout.strip())


def extract_release_notes(file: str | Path) -> str:
    """
    Extract release notes from a given file.

    Args:
        file: from which the release notes shall be extracted

    Returns:
        A string containing the cleaned release notes extracted from the file.
    """
    with open(file) as f:
        lines = f.readlines()[1:]
        content = "".join(lines)
        content = cleandoc(content)
        content += "\n"
    return content


def new_changes(file: str | Path, version: Version) -> str:
    """
    Create a new changelog list, adding the provided version to it.

    Args:
        file: containing the old changelog list.
        version: of the new entry to add to the list.

    Returns:
        Content for the new changelog list.
    """
    file = Path(file)
    content = []

    with open(file) as f:
        for line in f:
            content.append(line)
            if line.startswith("* [unreleased]"):
                content.append(f"* [{version}](changes_{version}.md)\n")
            if line.startswith("unreleased"):
                content.append(f"changes_{version}\n")

    return "".join(content)


def new_unreleased() -> str:
    """
    Generates the content for a new Unreleased changelog file.

    Returns:
        A string representing the content for an empty Unreleased changelog file.
    """
    return "# Unreleased\n"


def new_changelog(version: Version, content: str, date: datetime | None = None) -> str:
    """
    Create a changelog entry for a specific version.

    Args:
        version: An instance of the Version class representing the release version.
        content: The content of the changelog entry.
        date: Optional. The release date. If not provided, the current date will be used.

    Returns:
        The generated changelog.
    """
    date = datetime.today() if date is None else date
    template = cleandoc(
        """
        # {version} - {date}

        {content}
        """
    )
    return template.format(
        version=version, date=date.strftime("%Y-%m-%d"), content=content
    )
