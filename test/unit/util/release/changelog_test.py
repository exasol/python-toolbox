from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.changelog import (
    UNRELEASED_INITIAL_CONTENT,
    Changelogs,
)
from exasol.toolbox.util.version import Version


class SampleContent:
    changelog = cleandoc(
        """
        ## Added
        * Added Awesome feature

        ## Changed
        * Some behaviour

        ## Fixed
        * Fixed nasty bug
        """
    )
    changes = cleandoc(
        """
        # Changelog

        * [unreleased](unreleased.md)
        * [0.1.0](changes_0.1.0.md)

        ```{toctree}
        ---
        hidden:
        ---
        unreleased
        changes_0.1.0
        ```
        """
    )
    altered_changes = cleandoc(
        """
        # Changelog

        * [unreleased](unreleased.md)
        * [1.0.0](changes_1.0.0.md)
        * [0.1.0](changes_0.1.0.md)

        ```{toctree}
        ---
        hidden:
        ---
        unreleased
        changes_1.0.0
        changes_0.1.0
        ```
        """
    )


@pytest.fixture(scope="function")
def changes_md(changelogs):
    changelogs.changelog_md.write_text(SampleContent.changes)


@pytest.fixture(scope="function")
def unreleased_md(changelogs):
    changelogs.unreleased_md.write_text(
        UNRELEASED_INITIAL_CONTENT + SampleContent.changelog
    )


@pytest.fixture(scope="function")
def changelogs(tmp_path) -> Changelogs:
    return Changelogs(changes_path=tmp_path, version=Version(major=1, minor=0, patch=0))


class TestChangelogs:
    """
    As some methods in the class `Changelogs` modify files, it is required that the
    fixtures which create the sample files (changelog.md, unreleased.md, & changes_1.0.0.md)
    reset per function and use `tmp_path`. By doing this, we ensure that the sample
    are in their expected state for each test.
    """

    @staticmethod
    def test_create_new_unreleased(changelogs):
        changelogs._create_new_unreleased()

        assert changelogs.unreleased_md.read_text() == UNRELEASED_INITIAL_CONTENT

    @staticmethod
    def test_create_versioned_changelog(changelogs):
        changelogs._create_versioned_changelog(SampleContent.changelog)
        saved_text = changelogs.versioned_changelog_md.read_text()

        assert "1.0.0" in saved_text
        assert SampleContent.changelog in saved_text

    @staticmethod
    def test_extract_unreleased_notes(changelogs, unreleased_md):
        result = changelogs._extract_unreleased_notes()

        assert result == SampleContent.changelog + "\n"

    @staticmethod
    def test_update_changelog_table_of_contents(changelogs, changes_md):
        changelogs._update_changelog_table_of_contents()

        assert changelogs.changelog_md.read_text() == SampleContent.altered_changes

    @staticmethod
    def test_update_changelogs_for_release(changelogs, unreleased_md, changes_md):
        changelogs.update_changelogs_for_release()

        # changes.md
        assert changelogs.changelog_md.read_text() == SampleContent.altered_changes
        # unreleased.md
        assert changelogs.unreleased_md.read_text() == UNRELEASED_INITIAL_CONTENT
        # versioned.md
        saved_text = changelogs.versioned_changelog_md.read_text()
        assert "1.0.0" in saved_text
        assert SampleContent.changelog in saved_text
