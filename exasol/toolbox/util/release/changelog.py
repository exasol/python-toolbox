from __future__ import annotations

from collections import OrderedDict
from collections.abc import Generator
from datetime import datetime
from inspect import cleandoc
from pathlib import Path

from exasol.toolbox.util.dependencies.audit import (
    get_vulnerabilities,
    get_vulnerabilities_from_latest_tag,
)
from exasol.toolbox.util.dependencies.poetry_dependencies import (
    get_dependencies,
    get_dependencies_from_latest_tag,
)
from exasol.toolbox.util.dependencies.shared_models import LatestTagNotFoundError
from exasol.toolbox.util.dependencies.track_changes import DependencyChanges
from exasol.toolbox.util.dependencies.track_vulnerabilities import DependenciesAudit
from exasol.toolbox.util.release.markdown import Markdown
from exasol.toolbox.util.version import Version

UNRELEASED_INITIAL_CONTENT = cleandoc("""
    # Unreleased

    ## Summary
    """) + "\n"


class Changelog:
    def __init__(self, changes_path: Path, root_path: Path, version: Version) -> None:
        """
        Args:
            changes_path: directory containing the changelog & changes files, e.g. `doc/changes/`
            root_path: root directory of the current project, containing file
                `pyproject.toml`
            version: the version to be used in the versioned changes file and listed in
                the `changelog.md`, which contains the index of the change log
        """

        self.version = version
        self.unreleased: Path = changes_path / "unreleased.md"
        self.versioned_changes: Path = changes_path / f"changes_{version}.md"
        # Accepting attribute changelog duplicating the class name
        self.changelog: Path = changes_path / "changelog.md" # NOSONAR
        self.root_path: Path = root_path

    def _create_new_unreleased(self):
        """
        Write a new unreleased changelog file.
        """

        self.unreleased.write_text(UNRELEASED_INITIAL_CONTENT)

    def _dependency_sections(self) -> Generator[Markdown]:
        """
        Return the dependency changes between the latest tag and the
        current version for use in the versioned changes file in markdown
        format. If there are no changes, return an empty string.
        """

        try:
            previous_groups = get_dependencies_from_latest_tag(root_path=self.root_path)
        except LatestTagNotFoundError:
            # In new projects, there is not a pre-existing tag, and all dependencies
            # are considered new.
            previous_groups = OrderedDict()

        current_groups = get_dependencies(working_directory=self.root_path)
        all_groups = previous_groups.keys() | current_groups.keys()

        for group in self._sort_groups(all_groups):
            previous = previous_groups.get(group, {})
            current = current_groups.get(group, {})
            if changes := DependencyChanges(
                previous_dependencies=previous,
                current_dependencies=current,
            ).changes:
                items = "\n".join(str(change) for change in changes)
                yield Markdown(f"### `{group}`", items=items)

    def _dependency_changes(self) -> Markdown | None:
        if sections := list(self._dependency_sections()):
            return Markdown("## Dependency Updates", children=sections)
        return None

    @staticmethod
    def _sort_groups(groups: set[str]) -> list[str]:
        """
        Prepare a deterministic sorting for groups shown in the versioned changes file:
            - `main` group should always be first
            - remaining groups are sorted alphabetically
        """

        main = "main"
        if main not in groups:
            # sorted converts set to list
            return sorted(groups)
        remaining_groups = groups - {main}
        # sorted converts set to list
        return [main] + sorted(remaining_groups)

    def _update_table_of_contents(self) -> None:
        """
        Read the existing `changelog.md`, append the latest changes file
        to the relevant sections, and write the updated changelog.md again.
        """
        updated_content = []
        with self.changelog.open(mode="r", encoding="utf-8") as f:
            for line in f:
                updated_content.append(line)
                if line.startswith("* [unreleased]"):
                    updated_content.append(
                        f"* [{self.version}](changes_{self.version}.md)\n"
                    )
                if line.startswith("unreleased"):
                    updated_content.append(f"changes_{self.version}\n")
        updated_content_str = "".join(updated_content)

        self.changelog.write_text(updated_content_str)

    def get_changed_files(self) -> list[Path]:
        return [self.unreleased, self.versioned_changes, self.changelog]

    def _resolved_vulnerabilities(self) -> Markdown | None:
        report = DependenciesAudit(
            previous_vulnerabilities=get_vulnerabilities_from_latest_tag(
                self.root_path
            ),
            current_vulnerabilities=get_vulnerabilities(self.root_path),
        ).report_resolved_vulnerabilities()
        return Markdown("## Security Issues", report) if report else None

    def _create_versioned_changes(self, initial_content: str) -> None:
        """
        Create a versioned changes file.

        Args:
            unreleased_content: the content of the (not yet versioned) changes
        """

        versioned = Markdown.from_text(initial_content)
        versioned.title = f"# {self.version} - {datetime.today().strftime('%Y-%m-%d')}"
        if dependency_changes := self._dependency_changes():
            versioned.replace_or_append_child(dependency_changes)
        if resolved_vulnerabilities := self._resolved_vulnerabilities():
            if section := versioned.child(resolved_vulnerabilities.title):
                section.intro = resolved_vulnerabilities.intro
            else:
                versioned.add_child(resolved_vulnerabilities)
        self.versioned_changes.write_text(versioned.rendered)

    def prepare_release(self) -> Changelog:
        """
        Rotates the changelogs as is needed for a release.

          1. Moves the contents from the `unreleased.md` to the `changes_<version>.md`
          2. Create a new file `unreleased.md`
          3. Updates the table of contents in the `changelog.md` with the new `changes_<version>.md`
        """

        content = self.unreleased.read_text()
        self._create_versioned_changes(content)

        # update other changelogs now that versioned changelog exists
        self._create_new_unreleased()
        self._update_table_of_contents()
        return self

    def update_latest(self) -> Changelog:
        """
        Update the updated dependencies in the latest versioned changelog.
        """

        content = self.versioned_changes.read_text()
        self._create_versioned_changes(content)
        return self
