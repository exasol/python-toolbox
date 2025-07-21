from __future__ import annotations

from datetime import datetime
from inspect import cleandoc
from pathlib import Path

from exasol.toolbox.util.version import Version

UNRELEASED_INITIAL_CONTENT = "# Unreleased\n"


class Changelogs:
    def __init__(self, changes_path: Path, version: Version) -> None:
        self.version = version
        self.unreleased_md: Path = changes_path / "unreleased.md"
        self.versioned_changelog_md: Path = changes_path / f"changes_{version}.md"
        self.changelog_md: Path = changes_path / "changelog.md"

    def _create_new_unreleased(self):
        """
        Write a new unreleased changelog file.
        """
        self.unreleased_md.write_text(UNRELEASED_INITIAL_CONTENT)

    def _create_versioned_changelog(self, content: str) -> None:
        """
        Create a changelog entry for a specific version.

        Args:
            content: The content of the changelog entry.

        """
        template = cleandoc(
            f"""
            # {self.version} - {datetime.today().strftime("%Y-%m-%d")}

            {content}
            """
        )
        self.versioned_changelog_md.write_text(template)

    def _extract_unreleased_notes(self) -> str:
        """
        Extract release notes from `unreleased.md`.
        """
        with self.unreleased_md.open(mode="r", encoding="utf-8") as f:
            # skip header when reading in file, as contains # Unreleased
            lines = f.readlines()[1:]
        unreleased_content = cleandoc("".join(lines))
        unreleased_content += "\n"
        return unreleased_content

    def _update_changelog_table_of_contents(self) -> None:
        """
        Read in existing `changelog.md` and append to appropriate sections
        before writing out to again.
        """
        updated_content = []
        with self.changelog_md.open(mode="r", encoding="utf-8") as f:
            for line in f:
                updated_content.append(line)
                if line.startswith("* [unreleased]"):
                    updated_content.append(
                        f"* [{self.version}](changes_{self.version}.md)\n"
                    )
                if line.startswith("unreleased"):
                    updated_content.append(f"changes_{self.version}\n")
        updated_content_str = "".join(updated_content)

        self.changelog_md.write_text(updated_content_str)

    def get_changed_files(self) -> list[Path]:
        return [self.unreleased_md, self.versioned_changelog_md, self.changelog_md]

    def update_changelogs_for_release(self) -> None:
        """
        Rotates the changelogs as is needed for a release.

          1. Moves the contents of the `unreleased.md` to the `changes_<version>.md`
          2. Create a new `unreleased.md`
          3. Updates the table of contents in the `changelog.md` with the new `changes_<version>.md`
        """

        # create versioned changelog
        unreleased_content = self._extract_unreleased_notes()
        self._create_versioned_changelog(unreleased_content)

        # update other changelogs now that versioned changelog exists
        self._create_new_unreleased()
        self._update_changelog_table_of_contents()
