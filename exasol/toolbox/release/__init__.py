from __future__ import annotations

from datetime import datetime
from inspect import cleandoc
from pathlib import Path

from exasol.toolbox.util.version import Version


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
