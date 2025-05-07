import pytest

import noxconfig
from exasol.toolbox.nox._shared import (
    DEFAULT_PATH_FILTERS,
    python_files,
)


@pytest.fixture(scope="session")
def package_directory():
    return "toolbox"


@pytest.fixture(scope="session")
def tmp_directory(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="session")
def path_filter_directory():
    return "path_filter"


@pytest.fixture(scope="session")
def directories(package_directory, path_filter_directory):
    yield DEFAULT_PATH_FILTERS.union({package_directory, path_filter_directory})


@pytest.fixture(scope="session")
def create_files(tmp_directory, directories):
    file_list = []
    for directory in directories:
        directory_path = tmp_directory / directory
        directory_path.mkdir(parents=True, exist_ok=True)

        file_path = directory_path / f"{directory}-dummy.py"
        file_path.touch()
        file_list.append(file_path)

    yield file_list


def test_python_files(
        tmp_directory, create_files, package_directory, path_filter_directory
):
    # Use builtin object to modify attribute path_filters of frozen dataclass instance.
    object.__setattr__(
        noxconfig.PROJECT_CONFIG, "path_filters", (path_filter_directory,)
    )

    actual = python_files(tmp_directory)
    assert len(actual) == 1
    assert actual[0].parent.name == package_directory
