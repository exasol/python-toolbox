import subprocess

import pytest

from exasol.toolbox.util.dependencies.poetry_dependencies import (
    PoetryDependencies,
    PoetryGroup,
    PoetryToml,
    get_dependencies,
    get_dependencies_from_latest_tag,
)
from exasol.toolbox.util.dependencies.shared_models import Package
from noxconfig import PROJECT_CONFIG

MAIN_GROUP = PoetryGroup(name="main", toml_section="project.dependencies")
DEV_GROUP = PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies")
ANALYSIS_GROUP = PoetryGroup(
    name="analysis", toml_section="tool.poetry.group.analysis.dependencies"
)

PYLINT = Package(name="pylint", version="3.3.7")
ISORT = Package(name="isort", version="6.0.1")
BLACK = Package(name="black", version="25.1.0")

DIRECT_DEPENDENCIES = {
    MAIN_GROUP.name: {PYLINT.name: PYLINT},
    DEV_GROUP.name: {ISORT.name: ISORT},
    ANALYSIS_GROUP.name: {BLACK.name: BLACK},
}


@pytest.fixture(scope="module")
def cwd(tmp_path_factory):
    return tmp_path_factory.mktemp("test")


@pytest.fixture(scope="module")
def project_name():
    return "project"


@pytest.fixture(scope="module")
def project_path(cwd, project_name):
    return cwd / project_name


@pytest.fixture(scope="module")
def create_poetry_project(cwd, project_name, project_path):
    subprocess.run(["poetry", "new", project_name], cwd=cwd)
    subprocess.run(
        ["poetry", "add", f"{PYLINT.name}=={PYLINT.version}"], cwd=project_path
    )
    subprocess.run(
        ["poetry", "add", "--group", "dev", f"{ISORT.name}=={ISORT.version}"],
        cwd=project_path,
    )
    subprocess.run(
        ["poetry", "add", "--group", "analysis", f"{BLACK.name}=={BLACK.version}"],
        cwd=project_path,
    )


@pytest.fixture(scope="module")
def pyproject_toml(project_path, create_poetry_project):
    return PoetryToml.load_from_toml(working_directory=project_path)


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


class TestPoetryDependencies:
    @staticmethod
    @pytest.mark.parametrize(
        "line,expected",
        [
            (
                "coverage                      7.8.0     Code coverage measurement for Python",
                Package(name="coverage", version="7.8.0"),
            ),
            (
                "furo                          2024.8.6  A clean customisable Sphinx documentation theme.",
                Package(name="furo", version="2024.8.6"),
            ),
            (
                "import-linter                 2.3       Enforces rules for the imports within and between Python packages.",
                Package(name="import-linter", version="2.3"),
            ),
            (
                "python-dateutil               2.9.0.post0     Extensions to the standard Python datetime module",
                Package(name="python-dateutil", version="2.9.0.post0"),
            ),
            (
                "types-requests                             2.32.0.20250602",
                Package(name="types-requests", version="2.32.0.20250602"),
            ),
        ],
    )
    def test_extract_from_line(line, expected):
        result = PoetryDependencies._extract_from_line(line=line)
        assert result == expected

    @staticmethod
    def test_direct_dependencies(create_poetry_project, project_path):
        poetry_dep = PoetryDependencies(
            groups=(MAIN_GROUP, DEV_GROUP, ANALYSIS_GROUP),
            working_directory=project_path,
        )
        assert poetry_dep.direct_dependencies == DIRECT_DEPENDENCIES

    @staticmethod
    def test_all_dependencies(create_poetry_project, project_path):
        poetry_dep = PoetryDependencies(
            groups=(MAIN_GROUP, DEV_GROUP, ANALYSIS_GROUP),
            working_directory=project_path,
        )
        result = poetry_dep.all_dependencies

        transitive = result.pop("transitive")
        assert len(transitive) > 0
        assert result == DIRECT_DEPENDENCIES


def test_get_dependencies():
    result = get_dependencies(PROJECT_CONFIG.root_path)

    # if successful, no errors & should be non-empty dictionary
    assert isinstance(result, dict)
    assert result.keys()


def test_get_dependencies_from_latest_tag():
    result = get_dependencies_from_latest_tag()

    # if successful, no errors & should be non-empty dictionary
    assert isinstance(result, dict)
    assert result.keys()
