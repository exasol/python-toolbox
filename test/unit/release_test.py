import subprocess
from unittest.mock import patch

import pytest

from exasol.toolbox.release import Version


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
        ("1.2.3", Version(1, 2, 0)),
        ("1.2", Version(1, 2, 0)),
        ("1", Version(1, 0, 0)),
    ],
)
def test_version_from_poetry(poetry_version, version, expected):
    with patch("subprocess.run", return_value=poetry_version(version)):
        actual = Version.from_poetry()

    assert expected == actual
