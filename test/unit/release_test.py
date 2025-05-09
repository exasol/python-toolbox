from datetime import datetime
from inspect import cleandoc
from subprocess import CalledProcessError
from unittest.mock import patch, MagicMock

import pytest

from exasol.toolbox.nox._release import _trigger_release, ReleaseError
from exasol.toolbox.release import (
    extract_release_notes,
    new_changelog,
)
from exasol.toolbox.util.version import Version


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
