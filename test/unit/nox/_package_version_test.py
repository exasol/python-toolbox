from unittest import mock

import pytest

from exasol.toolbox.nox._package_version import (
    _create_parser,
    _version_check,
    write_version_module,
)
from exasol.toolbox.util.version import Version
from noxconfig import (
    Config,
)

DEFAULT_VERSION = Version(major=0, minor=1, patch=0)
ALTERNATE_VERSION = Version(major=0, minor=2, patch=0)


@pytest.fixture
def config(version_file) -> Config:
    return Config(version_file=version_file)


@pytest.fixture
def version_file(tmp_path):
    version_file = tmp_path / "version.py"
    write_version_module(version=DEFAULT_VERSION, version_file=version_file)
    return version_file


def test_write_version_module(version_file) -> None:
    write_version_module(version=ALTERNATE_VERSION, version_file=version_file)
    assert version_file.exists()

    with version_file.open(mode="r", encoding="utf-8") as f:
        result = f.read()
    assert "MAJOR = 0\nMINOR = 2\nPATCH = 0\n" in result


class TestVersionCheck:
    @staticmethod
    @mock.patch.object(Version, "from_poetry", return_value=DEFAULT_VERSION)
    def test_same_value_is_successful(from_poetry, config):
        Version(major=0, minor=1, patch=0)
        parser = _create_parser()
        args = parser.parse_args([])

        result = _version_check(args=args, config=config)
        assert result == 0

    @staticmethod
    @mock.patch.object(Version, "from_poetry", return_value=ALTERNATE_VERSION)
    def test_different_value_is_failure(from_poetry, config):
        Version(major=0, minor=1, patch=0)
        parser = _create_parser()
        args = parser.parse_args([])

        result = _version_check(args=args, config=config)
        assert result == 1

    @staticmethod
    @mock.patch.object(Version, "from_poetry", return_value=ALTERNATE_VERSION)
    def test_with_fix(from_poetry, config, version_file):
        parser = _create_parser()
        args = parser.parse_args(["--fix"])

        result = _version_check(args=args, config=config)
        assert result == 0
