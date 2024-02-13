from datetime import datetime
import subprocess
from inspect import cleandoc
from dataclasses import dataclass
from functools import total_ordering
from shutil import which

from exasol.toolbox.error import ToolboxError


def _index_or(container, index, default):
    try:
        return container[index]
    except IndexError:
        return default


@total_ordering
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other):
        return (
            self.major < other.major
            or (self.major <= other.major and self.minor < other.minor)
            or (
                self.major <= other.major
                and self.minor <= other.minor
                and self.patch < other.patch
            )
        )

    def __eq__(self, other):
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    @staticmethod
    def from_string(version):
        parts = [int(number, base=0) for number in version.split(".")]
        version = [_index_or(parts, i, 0) for i in range(3)]
        return Version(*version)

    @staticmethod
    def from_poetry():
        poetry = which("poetry")
        if not poetry:
            raise ToolboxError("Couldn't find poetry executable")

        try:
            result = subprocess.run(
                [poetry, "version", "--no-ansi", "--short"], capture_output=True
            )
        except subprocess.CalledProcessError as ex:
            raise ToolboxError() from ex
        version = result.stdout.decode().strip()

        return Version.from_string(version)


def changelog(version : Version, content: str, date: datetime | None = None) -> str:
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
        version=version,
        date=date.strftime('%Y-%m-%d'),
        content=content
    )
