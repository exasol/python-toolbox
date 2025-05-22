import subprocess
from pathlib import Path

import pytest

from toolbox.util.dependencies import PoetryToml, PoetryGroup

MAIN_GROUP = PoetryGroup(name="main", toml_section="project.dependencies")
DEV_GROUP = PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies")
ANALYSIS_GROUP =  PoetryGroup(name="analysis",
                            toml_section="tool.poetry.group.analysis.dependencies")


@pytest.fixture(scope="module")
def pyproject_toml_path(tmp_path_factory) -> Path:
    project_name = "project"
    path = tmp_path_factory.mktemp("test")
    subprocess.run(["poetry", "new", project_name], cwd=path)

    project_path = path / project_name
    subprocess.run(["poetry", "add", "numpy"], cwd=project_path)
    subprocess.run(["poetry", "add", "pylint"], cwd=project_path)
    subprocess.run(["poetry", "add", "--group", "dev", "isort"], cwd=project_path)
    subprocess.run(["poetry", "add", "--group", "analysis", "black"], cwd=project_path)
    return project_path / "pyproject.toml"


@pytest.fixture(scope="module")
def pyproject_toml(pyproject_toml_path):
    return PoetryToml(file_path=pyproject_toml_path)


class TestPoetryToml:
    @staticmethod
    def test_get_section_dict_exists(pyproject_toml):
        result = pyproject_toml.get_section_dict("project")
        assert result is not None

    @staticmethod
    def test_get_section_dict_does_not_exist(pyproject_toml):
        result = pyproject_toml.get_section_dict("test")
        assert result is None

    @staticmethod
    def test_groups(pyproject_toml):
        assert pyproject_toml.groups == (MAIN_GROUP, DEV_GROUP, ANALYSIS_GROUP)