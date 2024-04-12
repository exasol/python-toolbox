import pytest

from exasol.toolbox.tools.replace_version import (
    is_update_required,
    update_version,
    update_versions,
)


@pytest.mark.parametrize(
    "line,matcher,expected",
    [
        ("hallo/world@all", "hallo", True),
        ("hallo/world@all", "foo", False),
        ("hallo/world/all", "hallo", False),
        ("hallo/world/all", "foo", False),
    ],
)
def test_is_update_required(line, matcher, expected):
    actual = is_update_required(line, matcher)
    assert actual == expected


@pytest.mark.parametrize(
    "line,version,expected",
    [
        ("hallo/world@1.2.3\n", "2.3.4", "hallo/world@2.3.4\n"),
        ("hallo/world@0.0.0\n", "9.9.9", "hallo/world@9.9.9\n"),
    ],
)
def test_update_required(line, version, expected):
    actual = update_version(line, version)
    assert actual == expected


@pytest.mark.parametrize(
    "lines,matcher,version,expected",
    [
        (
            [
                "hallo/world@3.4.5\n",
                "foo/world@3.4.5\n",
                "hallo/world/3.4.5\n",
                "foo/world/3.4.5\n",
            ],
            "hallo",
            "4.5.6",
            [
                "hallo/world@4.5.6\n",
                "foo/world@3.4.5\n",
                "hallo/world/3.4.5\n",
                "foo/world/3.4.5\n",
            ],
        )
    ],
)
def test_update_versions(lines, matcher, version, expected):
    actual = update_versions(lines, matcher, version)
    assert actual == expected
