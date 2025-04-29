import subprocess
from subprocess import CalledProcessError
from unittest.mock import patch, MagicMock

import pytest

from exasol.toolbox.error import ToolboxError
from exasol.toolbox.nox._release import _trigger_release, ReleaseError
from exasol.toolbox.version import Version, poetry_command


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


@pytest.fixture(scope="class")
def mock_from_poetry():
    with patch(
        "exasol.toolbox.nox._release.Version.from_poetry", return_value="0.3.0"
    ) as mock_obj:
        yield mock_obj


class TestTriggerReleaseWithMocking:
    @staticmethod
    def _get_mock_string(args) -> str:
        if args == ("git", "remote", "show", "origin"):
            return "test\nHEAD branch: main\ntest"
        if args in [("git", "tag", "--list"), ("gh", "release", "list")]:
            return "0.1.0\n0.2.0"
        return ""

    def _get_subprocess_run_mock(self, args) -> str:
        return MagicMock(returncode=0, stdout=self._get_mock_string(args))

    def test_works_as_expected(self, mock_from_poetry):
        def simulate_pass(args, **kwargs):
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_pass):
            result = _trigger_release()
        assert result == mock_from_poetry.return_value

    @pytest.mark.parametrize(
        "error_cmd",
        [
            ("git", "remote", "show", "origin"),
            ("git", "checkout", "main"),
            ("git", "pull"),
            ("git", "tag", "--list"),
            ("gh", "release", "list"),
            ("git", "tag", "0.3.0"),
            ("git", "push", "origin", "0.3.0"),
        ],
    )
    def test_caught_called_process_error_raises_release_error(
        self, mock_from_poetry, error_cmd
    ):
        def simulate_fail(args, **kwargs):
            if args == error_cmd:
                raise CalledProcessError(returncode=1, cmd=error_cmd)
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_fail):
            with pytest.raises(ReleaseError) as ex:
                _trigger_release()
        assert str(error_cmd) in str(ex)

    def test_default_branch_could_not_be_found(self, mock_from_poetry):
        def simulate_fail(args, **kwargs):
            if args == ("git", "remote", "show", "origin"):
                return MagicMock(returncode=0, stdout="DUMMY TEXT")
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_fail):
            with pytest.raises(ReleaseError) as ex:
                _trigger_release()
        assert "default branch could not be found" in str(ex)

    def test_tag_already_exists(self, mock_from_poetry):
        version = mock_from_poetry.return_value

        def simulate_fail(args, **kwargs):
            if args == ("git", "tag", "--list"):
                return MagicMock(returncode=0, stdout=f"0.1.0\n0.2.0\n{version}")
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_fail):
            with pytest.raises(ReleaseError) as ex:
                _trigger_release()
        assert f"tag {version} already exists" in str(ex)

    def test_release_already_exists(self, mock_from_poetry):
        version = mock_from_poetry.return_value

        def simulate_fail(args, **kwargs):
            if args == ("gh", "release", "list"):
                return MagicMock(returncode=0, stdout=f"0.1.0\n0.2.0\n{version}")
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_fail):
            with pytest.raises(ReleaseError) as ex:
                _trigger_release()
        assert f"release {version} already exists" in str(ex)


@patch("exasol.toolbox.release.which", return_value=None)
def test_poetry_decorator_no_poetry_executable(mock):
    @poetry_command
    def test():
        pass

    with pytest.raises(ToolboxError):
        test()


@patch("exasol.toolbox.release.which", return_value="test/path")
def test_poetry_decorator_subprocess(mock):
    @poetry_command
    def test():
        raise subprocess.CalledProcessError(returncode=1, cmd=["test"])
        pass

    with pytest.raises(ToolboxError):
        test()
