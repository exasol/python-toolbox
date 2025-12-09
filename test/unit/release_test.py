from subprocess import CalledProcessError
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest

import noxconfig
from exasol.toolbox.nox._release import (
    ReleaseError,
    _trigger_release,
)
from exasol.toolbox.util.version import Version


@pytest.fixture(scope="class")
def mock_from_poetry():
    with patch(
        "exasol.toolbox.nox._release.Version.from_poetry",
        return_value=Version(major=0, minor=3, patch=0),
    ) as mock_obj:
        yield mock_obj


class TestTriggerReleaseWithMocking:
    @staticmethod
    def _get_mock_string(args) -> str:
        if args == ("git", "remote", "show", "origin"):
            return "test\nHEAD branch: main\ntest"
        if args == ("git", "tag", "--list"):
            return "0.1.0\n0.2.0"
        return ""

    def _get_subprocess_run_mock(self, args) -> str:
        return MagicMock(returncode=0, stdout=self._get_mock_string(args))

    def test_works_as_expected(self, mock_from_poetry):
        def simulate_pass(args, **kwargs):
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_pass):
            result = _trigger_release(noxconfig.PROJECT_CONFIG)
        assert result == mock_from_poetry.return_value

    def test_creates_major_version_tag(self, mock_from_poetry):
        def simulate_pass(args, **kwargs):
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_pass) as subprocess_mock:
            result = _trigger_release(noxconfig.PROJECT_CONFIG)
            commands = [c.args[0] for c in subprocess_mock.mock_calls]
            assert commands == [
                ("git", "remote", "show", "origin"),
                ("git", "checkout", "main"),
                ("git", "pull"),
                ("git", "fetch", "--all"),
                ("git", "tag", "--list"),
                ("git", "tag", "0.3.0"),
                ("git", "push", "origin", "0.3.0"),
                ("git", "tag", "-f", "v0"),
                ("git", "push", "-f", "origin", "v0"),
            ]
        assert result == mock_from_poetry.return_value

    def test_not_creates_major_version_tag(
        self, test_project_config_factory, mock_from_poetry
    ):

        def simulate_pass(args, **kwargs):
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_pass) as subprocess_mock:
            result = _trigger_release(project_config=test_project_config_factory())
            commands = [c.args[0] for c in subprocess_mock.mock_calls]
            assert commands == [
                ("git", "remote", "show", "origin"),
                ("git", "checkout", "main"),
                ("git", "pull"),
                ("git", "fetch", "--all"),
                ("git", "tag", "--list"),
                ("git", "tag", "0.3.0"),
                ("git", "push", "origin", "0.3.0"),
            ]
        assert result == mock_from_poetry.return_value

    @pytest.mark.parametrize(
        "error_cmd",
        [
            ("git", "remote", "show", "origin"),
            ("git", "checkout", "main"),
            ("git", "pull"),
            ("git", "tag", "--list"),
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
                _trigger_release(noxconfig.PROJECT_CONFIG)
        assert str(error_cmd) in str(ex)

    def test_default_branch_could_not_be_found(self, mock_from_poetry):
        def simulate_fail(args, **kwargs):
            if args == ("git", "remote", "show", "origin"):
                return MagicMock(returncode=0, stdout="DUMMY TEXT")
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_fail):
            with pytest.raises(ReleaseError) as ex:
                _trigger_release(noxconfig.PROJECT_CONFIG)
        assert "default branch could not be found" in str(ex)

    def test_tag_already_exists(self, mock_from_poetry):
        version = mock_from_poetry.return_value

        def simulate_fail(args, **kwargs):
            if args == ("git", "tag", "--list"):
                return MagicMock(returncode=0, stdout=f"0.1.0\n0.2.0\n{version}")
            return self._get_subprocess_run_mock(args)

        with patch("subprocess.run", side_effect=simulate_fail):
            with pytest.raises(ReleaseError) as ex:
                _trigger_release(noxconfig.PROJECT_CONFIG)
        assert f"tag {version} already exists" in str(ex)
