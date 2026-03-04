from pathlib import Path
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
    config = test_project_config_factory()
    additional = {
        config.root_path / d for d in (package_directory, excluded_python_path)
    }
    yield set(config.excluded_python_paths).union(additional)


@pytest.fixture
def create_files(tmp_path, directories: list[Path]) -> list[Path]:
    result = []
    for path in directories:
        # Expected to be ignored if its parent directory is configured as
        # excluded.
        sample = f"{path.name}/sample.py"

        # Expected to be included, as using parent.name only as substring of its
        # file name.
        included_1 = f"{path.name}_2_included.py"

        # Expected to be included, as having a different parent directory.
        included_2 = f"other/{path.name}/2_included.py"

        for relative in [sample, included_1, included_2]:
            file = path.parent / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            file.touch()
            result.append(file)

    return result


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

    assert len(actual) == 19
    exceptions = [f for f in actual if f.endswith("sample.py")]
    assert len(exceptions) == 1
    assert "toolbox/sample.py" in exceptions[0]
