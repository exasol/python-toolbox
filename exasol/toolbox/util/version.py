from __future__ import annotations

import subprocess
from dataclasses import dataclass
from enum import Enum
from functools import (
    total_ordering,
    wraps,
)
from pathlib import Path
from shutil import which
from typing import Any

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

    @staticmethod
    def from_python_module(path: Path) -> Version:
        """Retrieve version information from the `version` module"""
        with open(path, encoding="utf-8") as file:
            _locals: dict[str, Any] = {}
            _globals: dict[str, Any] = {}
            exec(file.read(), _locals, _globals)

            try:
                version = _globals["VERSION"]
            except KeyError as ex:
                raise ToolboxError("Couldn't find version within module") from ex

            return Version.from_string(version)
