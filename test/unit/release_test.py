import subprocess
from datetime import datetime
from inspect import cleandoc
from unittest.mock import patch

import pytest

from exasol.toolbox.nox._release import (
    ReleaseTypes,
    _type_release,
)
from exasol.toolbox.release import (
    Version,
    extract_release_notes,
    new_changelog,
)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("1.2.3", Version(1, 2, 3)),
        ("1.2", Version(1, 2, 0)),
        ("1", Version(1, 0, 0)),
    ],
)
def test_create_version_from_string(input, expected):
    actual = Version.from_string(input)
    assert expected == actual


@pytest.mark.parametrize(
    "old_version,new_version,expected",
    [
        (Version(1, 2, 3), Version(1, 2, 4), True),
        (Version(1, 2, 3), Version(1, 3, 3), True),
        (Version(1, 2, 3), Version(2, 2, 3), True),
        (Version(1, 2, 3), Version(1, 1, 3), False),
        (Version(1, 2, 3), Version(1, 2, 1), False),
        (Version(1, 2, 3), Version(0, 3, 3), False),
    ],
)
def test_is_later_version(old_version, new_version, expected):
    actual = new_version > old_version
    assert expected == actual


@pytest.fixture
def poetry_version():
    def set_poetry_version(version):
        return subprocess.CompletedProcess(
            args=["poetry", "version", "--no-ansi", "--short"],
            returncode=0,
            stdout=version.encode("utf8"),
            stderr="",
        )

    yield set_poetry_version


@pytest.mark.parametrize(
    "version,expected",
    [
        ("1.2.3", Version(1, 2, 3)),
        ("1.2", Version(1, 2, 0)),
        ("1", Version(1, 0, 0)),
    ],
)
def test_version_from_poetry(poetry_version, version, expected):
    with patch("subprocess.run", return_value=poetry_version(version)):
        actual = Version.from_poetry()

    assert expected == actual


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


@pytest.mark.parametrize(
    "rtype,old,expected",
    [
        ("major", "1.2.3", "2.0.0"),
        ("minor", "1.2.3", "1.3.0"),
        ("patch", "1.2.3", "1.2.4"),
    ],
)
def test_type_release(rtype, old, expected):
    actual = _type_release(ReleaseTypes(rtype), Version.from_string(old))
    expected = Version.from_string(expected)
    assert actual == expected
