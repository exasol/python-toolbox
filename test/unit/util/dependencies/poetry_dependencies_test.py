from inspect import cleandoc

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
GROUPS = (
    MAIN_GROUP,
    PoetryGroup(name="dev", toml_section="dependency-groups.dev"),
    PoetryGroup(name="analysis", toml_section="dependency-groups.analysis"),
)


@pytest.fixture(scope="module")
def new_pyproject_toml(project_path, create_new_poetry_project):
    return PoetryToml.load_from_toml(working_directory=project_path)


@pytest.fixture(scope="module")
def poetry_2_1_pyproject_toml(cwd, poetry_2_1_pyproject_text):
    older_project_path = cwd / "older_project"
    older_project_path.mkdir(parents=True, exist_ok=True)
    pyproject_toml_path = older_project_path / "pyproject.toml"
    pyproject_toml_path.write_text(cleandoc(poetry_2_1_pyproject_text))
    return PoetryToml.load_from_toml(working_directory=older_project_path)


@pytest.mark.slow
class TestPoetryToml:
    @staticmethod
    def test_get_section_dict_exists(new_pyproject_toml):
        result = new_pyproject_toml.get_section_dict("project")
        assert result is not None

    @staticmethod
    def test_get_section_dict_does_not_exist(new_pyproject_toml):
        result = new_pyproject_toml.get_section_dict("test")
        assert result is None

    @staticmethod
    def test_groups(new_pyproject_toml):
        assert new_pyproject_toml.groups == GROUPS

    @staticmethod
    def test_groups_with_poetry_2_1_0(poetry_2_1_pyproject_toml):
        assert poetry_2_1_pyproject_toml.groups == (
            MAIN_GROUP,
            PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies"),
            PoetryGroup(
                name="analysis", toml_section="tool.poetry.group.analysis.dependencies"
            ),
        )


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

    @pytest.mark.slow
    @staticmethod
    def test_direct_dependencies(
        create_new_poetry_project, project_path, sample_versions
    ):
        poetry_dep = PoetryDependencies(
            groups=GROUPS,
            working_directory=project_path,
        )
        assert poetry_dep.direct_dependencies == {
            "main": {
                "pylint": Package(name="pylint", version=sample_versions.pylint),
                "ruff": Package(name="ruff", version=sample_versions.ruff),
            },
            "dev": {"isort": Package(name="isort", version=sample_versions.isort)},
            "analysis": {"black": Package(name="black", version=sample_versions.black)},
        }

    @pytest.mark.slow
    @staticmethod
    def test_all_dependencies(create_new_poetry_project, project_path, sample_versions):
        poetry_dep = PoetryDependencies(
            groups=GROUPS,
            working_directory=project_path,
        )
        result = poetry_dep.all_dependencies

        transitive = result.pop("transitive")
        assert len(transitive) > 0
        assert result == {
            "main": {
                "pylint": Package(name="pylint", version=sample_versions.pylint),
                "ruff": Package(name="ruff", version=sample_versions.ruff),
            },
            "dev": {"isort": Package(name="isort", version=sample_versions.isort)},
            "analysis": {"black": Package(name="black", version=sample_versions.black)},
        }


@pytest.mark.slow
def test_get_dependencies():
    result = get_dependencies(PROJECT_CONFIG.root_path)

    # if successful, no errors & should be non-empty dictionary
    assert isinstance(result, dict)
    assert result.keys()


@pytest.mark.slow
def test_get_dependencies_from_latest_tag():
    result = get_dependencies_from_latest_tag(root_path=PROJECT_CONFIG.root_path)

    # if successful, no errors & should be non-empty dictionary
    assert isinstance(result, dict)
    assert result.keys()
