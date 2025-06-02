import subprocess
from unittest.mock import patch

import pytest

from exasol.toolbox.error import ToolboxError
from exasol.toolbox.util.version import (
    Version,
    poetry_command,
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
            stdout=version,
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


@patch("exasol.toolbox.util.version.which", return_value=None)
def test_poetry_decorator_no_poetry_executable(mock):
    @poetry_command
    def test():
        pass

    with pytest.raises(ToolboxError):
        test()


@patch("exasol.toolbox.util.version.which", return_value="test/path")
def test_poetry_decorator_subprocess(mock):
    @poetry_command
    def test():
        raise subprocess.CalledProcessError(returncode=1, cmd=["test"])
        pass

    with pytest.raises(ToolboxError):
        test()


def test_version_from_python_module(tmp_path):
    tmp_file = tmp_path / "file"
    file = """
MAJOR = 1
MINOR = 2
PATCH = 3
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"
__version__ = VERSION
    """
    tmp_file.write_text(file)
    assert Version.from_python_module(tmp_file) == Version.from_string("1.2.3")


def test_version_from_python_no_module_error(tmp_path):
    file_path = tmp_path / "file"
    file_path.write_text("")
    with pytest.raises(ToolboxError) as ex:
        Version.from_python_module(file_path)
    assert str(ex.value) == "Couldn't find version within module"
