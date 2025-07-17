import pytest
from packaging.version import Version

from exasol.toolbox.util.git import Git

POETRY_LOCK = "poetry.lock"


@pytest.fixture(scope="module")
def latest_tag() -> str:
    return Git.get_latest_tag()


@pytest.fixture(scope="module")
def read_file_from_tag(latest_tag) -> str:
    return Git.read_file_from_tag(tag=latest_tag, remote_file=POETRY_LOCK)


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
    def test_copy_remote_file_locally(tmp_path, read_file_from_tag):
        latest_tag = Git.get_latest_tag()

        Git.copy_remote_file_locally(
            tag=latest_tag, remote_file=POETRY_LOCK, destination_directory=tmp_path
        )

        result = (tmp_path / POETRY_LOCK).read_text()
        assert result == read_file_from_tag
