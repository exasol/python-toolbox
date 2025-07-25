from __future__ import annotations

from datetime import datetime
from inspect import cleandoc
from itertools import chain
from pathlib import Path

from exasol.toolbox.util.dependencies.poetry_dependencies import (
    get_dependencies,
    get_dependencies_from_latest_tag,
)
from exasol.toolbox.util.dependencies.track_changes import DependencyChanges
from exasol.toolbox.util.version import Version

UNRELEASED_INITIAL_CONTENT = "# Unreleased\n"


class Changelogs:
    def __init__(self, changes_path: Path, root_path: Path, version: Version) -> None:
        """
        Args:
            changes_path: directory containing the changelog, e.g. `doc/changes/`
            root_path: root directory of the current project, containing file
                `pyproject.toml`
            version: the version to be used in the `changes_{version}.md` and listed in the `changelog.md`.
        """

        self.version = version
        self.unreleased_md: Path = changes_path / "unreleased.md"
        self.versioned_changelog_md: Path = changes_path / f"changes_{version}.md"
        self.changelog_md: Path = changes_path / "changelog.md"
        self.root_path: Path = root_path

    def _create_new_unreleased(self):
        """
        Write a new unreleased changelog file.
        """
        self.unreleased_md.write_text(UNRELEASED_INITIAL_CONTENT)

    def _create_versioned_changelog(self, unreleased_content: str) -> None:
        """
        Create a changelog entry for a specific version.

        Args:
            unreleased_content: The content of the changelog entry.

        """
        template = f"# {self.version} - {datetime.today().strftime('%Y-%m-%d')}"
        template += f"\n{unreleased_content}"

        if dependency_content := self._prepare_dependency_update():
            template += f"\n## Dependency Updates\n{dependency_content}"

        self.versioned_changelog_md.write_text(cleandoc(template))

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

    def _prepare_dependency_update(self) -> str:
        previous_dependencies_in_groups = get_dependencies_from_latest_tag()
        current_dependencies_in_groups = get_dependencies(
            working_directory=self.root_path
        )

        content = ""
        # preserve order of keys from old group
        groups = list(
            dict.fromkeys(
                chain(
                    previous_dependencies_in_groups.keys(),
                    current_dependencies_in_groups.keys(),
                )
            )
        )
        for group in groups:
            previous_dependencies = previous_dependencies_in_groups.get(group, {})
            current_dependencies = current_dependencies_in_groups.get(group, {})
            changes = DependencyChanges(
                previous_dependencies=previous_dependencies,
                current_dependencies=current_dependencies,
            ).changes
            if changes:
                content += f"\n### `{group}`\n"
                content += "\n".join(str(change) for change in changes)
                content += "\n"
        return content

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
          2. Create a new file `unreleased.md`
          3. Updates the table of contents in the `changelog.md` with the new `changes_<version>.md`
        """

        # create versioned changelog
        unreleased_content = self._extract_unreleased_notes()
        self._create_versioned_changelog(unreleased_content)

        # update other changelogs now that versioned changelog exists
        self._create_new_unreleased()
        self._update_changelog_table_of_contents()
