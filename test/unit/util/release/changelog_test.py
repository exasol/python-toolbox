from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.changelog import (
    UNRELEASED_TEXT,
    Changelogs,
)
from exasol.toolbox.util.version import Version

CHANGES_CONTENTS = cleandoc(
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

ALTERED_CHANGES_CONTENTS = cleandoc(
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

SHARED_TEXT = cleandoc(
    """
    ## Added
    * Added Awesome feature

    ## Changed
    * Some behaviour

    ## Fixed
    * Fixed nasty bug
    """
)


@pytest.fixture
def changes_md(tmp_path, changelogs):
    """
    As some operations in Changelogs modify files, we need a reset per function
    """
    changelogs.changes_md.write_text(CHANGES_CONTENTS)


@pytest.fixture
def unreleased_md(tmp_path, changelogs):
    """
    As some operations in Changelogs modify files, we need a reset per function
    """
    changelogs.unreleased_md.write_text(UNRELEASED_TEXT + SHARED_TEXT)


@pytest.fixture
def changelogs(tmp_path) -> Changelogs:
    """
    As some operations in Changelogs modify files, we need a reset per function
    """
    return Changelogs(changes_path=tmp_path, version=Version(major=1, minor=0, patch=0))


class TestChangelogs:
    @staticmethod
    def test_create_new_unreleased(changelogs):
        changelogs._create_new_unreleased()

        assert changelogs.unreleased_md.read_text() == UNRELEASED_TEXT

    @staticmethod
    def test_create_versioned_changelog(changelogs):
        changelogs._create_versioned_changelog(SHARED_TEXT)
        saved_text = changelogs.versioned_changelog_md.read_text()

        assert "1.0.0" in saved_text
        assert SHARED_TEXT in saved_text

    @staticmethod
    def test_extract_unreleased_notes(changelogs, unreleased_md):
        result = changelogs._extract_unreleased_notes()

        assert result == SHARED_TEXT + "\n"

    @staticmethod
    def test_update_changelog_table_of_contents(changelogs, changes_md):
        changelogs._update_changelog_table_of_contents()

        assert changelogs.changes_md.read_text() == ALTERED_CHANGES_CONTENTS

    @staticmethod
    def test_update_changelogs_for_release(changelogs, unreleased_md, changes_md):
        changelogs.update_changelogs_for_release()

        # changes.md
        assert changelogs.changes_md.read_text() == ALTERED_CHANGES_CONTENTS
        # unreleased.md
        assert changelogs.unreleased_md.read_text() == UNRELEASED_TEXT
        # versioned.md
        saved_text = changelogs.versioned_changelog_md.read_text()
        assert "1.0.0" in saved_text
        assert SHARED_TEXT in saved_text
