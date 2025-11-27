from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._shared import (
    check_for_config_attribute,
    get_filtered_python_files,
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
    yield set(BaseConfig().excluded_python_paths).union(
        {package_directory, path_filter_directory}
    )


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


def test_get_filtered_python_files(
    tmp_directory, create_files, package_directory, path_filter_directory
):
    config = BaseConfig(add_to_excluded_python_paths=(path_filter_directory,))

    with patch("exasol.toolbox.nox._shared.PROJECT_CONFIG", config):
        actual = get_filtered_python_files(tmp_directory)

    assert len(actual) == 1
    assert "toolbox-dummy" in actual[0]


@dataclass(frozen=True)
class PreviousConfig:
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    source: Path = Path("exasol/toolbox")
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    path_filters: Iterable[str] = ()
    pyupgrade_args: Iterable[str] = ("--py310-plus",)
    plugins = []


# attributes + properties
MIGRATED_VALUES = [
    *BaseConfig.model_fields.keys(),
    *BaseConfig.model_computed_fields.keys(),
]


class TestCheckForConfigAttribute:

    @pytest.mark.parametrize("attribute", MIGRATED_VALUES)
    def test_old_implementation_raises_error(self, attribute):
        with pytest.raises(
            AttributeError, match="from `exasol.toolbox.config.BaseConfig`"
        ):
            check_for_config_attribute(PreviousConfig(), attribute=attribute)

    @pytest.mark.parametrize("attribute", MIGRATED_VALUES)
    def test_current_implementation_passes(self, attribute):
        check_for_config_attribute(BaseConfig(), attribute=attribute)
