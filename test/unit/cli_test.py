from argparse import ArgumentTypeError

import pytest

from exasol.toolbox.cli import version
from exasol.toolbox.release import Version


@pytest.mark.parametrize(
    "version_string,expected_error",
    [
        ("1.b.a", ArgumentTypeError),
        ("F.b.a", ArgumentTypeError),
        ("F", ArgumentTypeError),
        ("Something", ArgumentTypeError),
        ("1.1.1b", ArgumentTypeError),
        ("1.1.1-pre", ArgumentTypeError),
    ],
)
def test_version_throws_exception_on_invalid_version_string(
    version_string, expected_error
):
    with pytest.raises(expected_error):
        _ = version(version_string)


@pytest.mark.parametrize(
    "version_string,expected",
    [
        ("1.2.3", Version(1, 2, 3)),
        ("1.0.0", Version(1, 0, 0)),
        ("1.0", Version(1, 0, 0)),
        ("1", Version(1, 0, 0)),
    ],
)
def test_version_gets_parsed_successfully(version_string, expected):
    actual = version(version_string)
    assert expected == actual
