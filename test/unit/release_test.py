from datetime import datetime
from inspect import cleandoc

import pytest

from exasol.toolbox.release import (
    extract_release_notes,
    new_changelog,
)
from exasol.toolbox.util import Version


@pytest.mark.parametrize(
    "version,content,date,expected",
    [
        (
            Version(0, 1, 0),
            cleandoc(
                """
                ## Added
                * Some great feature

                ## Refactored
                * Replaced xyz
                """
            ),
            datetime(2024, 2, 7),
            cleandoc(
                """
                # 0.1.0 - 2024-02-07

                ## Added
                * Some great feature

                ## Refactored
                * Replaced xyz
                """
            ),
        ),
    ],
)
def test_changelog(version, content, date, expected):
    actual = new_changelog(version, content, date)
    assert expected == actual


@pytest.fixture
def unreleased_md(tmp_path):
    file = tmp_path / "unreleased.md"
    file.write_text(
        cleandoc(
            """
        # Unreleased

        ## ✨ Added
        * Added Awesome feature

        ## 🔧 Changed
        * Some behaviour

        ## 🐞 Fixed
        * Fixed nasty bug
        """
        )
    )
    yield file


def test_extract_release_notes(unreleased_md):
    expected = (
        cleandoc(
            """
        ## ✨ Added
        * Added Awesome feature

        ## 🔧 Changed
        * Some behaviour

        ## 🐞 Fixed
        * Fixed nasty bug
        """
        )
        + "\n"
    )
    actual = extract_release_notes(unreleased_md)
    assert expected == actual
