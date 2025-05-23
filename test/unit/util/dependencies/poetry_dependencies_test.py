import subprocess

import pytest
from toolbox.util.dependencies.poetry_dependencies import (
    PoetryDependencies,
    PoetryDependency,
    PoetryGroup,
    PoetryToml,
)

MAIN_GROUP = PoetryGroup(name="main", toml_section="project.dependencies")
DEV_GROUP = PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies")
ANALYSIS_GROUP = PoetryGroup(
    name="analysis", toml_section="tool.poetry.group.analysis.dependencies"
)

DIRECT_DEPENDENCIES = {
    MAIN_GROUP.name: [
        PoetryDependency(name="numpy", version="2.2.6", group=MAIN_GROUP),
        PoetryDependency(name="pylint", version="3.3.7", group=MAIN_GROUP),
    ],
    DEV_GROUP.name: [PoetryDependency(name="isort", version="6.0.1", group=DEV_GROUP)],
    ANALYSIS_GROUP.name: [
        PoetryDependency(name="black", version="25.1.0", group=ANALYSIS_GROUP)
    ],
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
    subprocess.run(["poetry", "add", "numpy"], cwd=project_path)
    subprocess.run(["poetry", "add", "pylint"], cwd=project_path)
    subprocess.run(["poetry", "add", "--group", "dev", "isort"], cwd=project_path)
    subprocess.run(["poetry", "add", "--group", "analysis", "black"], cwd=project_path)


@pytest.fixture(scope="module")
def pyproject_toml(project_path, create_poetry_project):
    return PoetryToml(working_directory=project_path)


class TestPackage:
    @staticmethod
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("numpy", "numpy"),
            ("sphinxcontrib-applehelp", "sphinxcontrib-applehelp"),
            ("Imaginary_package", "imaginary-package"),
        ],
    )
    def test_normalized_name(name, expected):
        dep = PoetryDependency(name=name, version="0.1.0", group=None)
        assert dep.normalized_name == expected


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
                PoetryDependency(name="coverage", version="7.8.0", group=MAIN_GROUP),
            ),
            (
                "furo                          2024.8.6  A clean customisable Sphinx documentation theme.",
                PoetryDependency(name="furo", version="2024.8.6", group=MAIN_GROUP),
            ),
            (
                "import-linter                 2.3       Enforces rules for the imports within and between Python packages.",
                PoetryDependency(name="import-linter", version="2.3", group=MAIN_GROUP),
            ),
        ],
    )
    def test_extract_from_line(line, expected):
        result = PoetryDependencies._extract_from_line(line=line, group=MAIN_GROUP)
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
        # set_direct_deps = set(DIRECT_DEPENDENCIES)

        poetry_dep = PoetryDependencies(
            groups=(MAIN_GROUP, DEV_GROUP, ANALYSIS_GROUP),
            working_directory=project_path,
        )
        result = poetry_dep.all_dependencies

        transitive = result.pop("transitive")
        assert len(transitive) > 0
        assert result == DIRECT_DEPENDENCIES
