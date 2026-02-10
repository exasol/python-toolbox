from unittest.mock import patch

import pytest

from exasol.toolbox.nox._shared import (
    get_filtered_python_files,
)


@pytest.fixture(scope="session")
def package_directory():
    return "toolbox"


@pytest.fixture(scope="session")
def tmp_directory(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="session")
def excluded_python_path():
    return "excluded_python_path"


@pytest.fixture
def directories(test_project_config_factory, package_directory, excluded_python_path):
    yield set(test_project_config_factory().excluded_python_paths).union(
        {package_directory, excluded_python_path}
    )


@pytest.fixture
def create_files(tmp_path, directories):
    file_list = []
    for directory in directories:
        directory_path = tmp_path / directory
        directory_path.mkdir(parents=True, exist_ok=True)

        file_path = directory_path / f"{directory}-dummy.py"
        file_path.touch()
        file_list.append(file_path)

    yield file_list


def test_get_filtered_python_files(
    test_project_config_factory,
    tmp_path,
    create_files,
    package_directory,
    excluded_python_path,
):
    config = test_project_config_factory(
        add_to_excluded_python_paths=(excluded_python_path,)
    )

    with patch("exasol.toolbox.nox._shared.PROJECT_CONFIG", config):
        actual = get_filtered_python_files(tmp_path)

    assert len(actual) == 1
    assert "toolbox-dummy" in actual[0]
