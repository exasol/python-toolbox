import subprocess

import pytest
from packaging.version import Version

from exasol.toolbox.util.git import Git

POETRY_LOCK = "poetry.lock"


@pytest.fixture(scope="module")
def latest_tag() -> str:
    return Git.get_latest_tag()


@pytest.fixture(scope="module")
def read_file_from_tag(latest_tag) -> str:
    return Git.read_file_from_tag(tag=latest_tag, path=POETRY_LOCK)


class TestGit:
    @staticmethod
    def test_latest_tag(latest_tag):
        assert isinstance(latest_tag, str)
        assert Version(latest_tag)

    @staticmethod
    def test_read_file_from_tag(read_file_from_tag):
        assert isinstance(read_file_from_tag, str)
        assert read_file_from_tag != ""

    @staticmethod
    def test_checkout(tmp_path, read_file_from_tag):
        tag = Git.get_latest_tag()
        dest = tmp_path / POETRY_LOCK
        Git.checkout(tag=tag, source=POETRY_LOCK, dest=dest)
        result = dest.read_text()
        assert result == read_file_from_tag

    @staticmethod
    def test_has_uncommitted_path_changes(tmp_path, monkeypatch):
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        monkeypatch.chdir(repo_path)

        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            check=True,
            capture_output=True,
        )

        test_file = repo_path / "test.txt"
        test_file.write_text("initial\n")
        subprocess.run(
            ["git", "add", "test.txt"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "initial commit"],
            check=True,
            capture_output=True,
        )

        assert Git.has_uncommitted_path_changes((test_file,)) is False

        test_file.write_text("changed\n")

        assert Git.has_uncommitted_path_changes((test_file,)) is True
