import subprocess
from enum import Enum

import pytest


class SampleVersions(str, Enum):
    black = "25.1.0"
    isort = "6.0.1"
    pylint = "3.3.7"
    ruff = "0.14.14"


@pytest.fixture(scope="module")
def sample_versions():
    return SampleVersions


@pytest.fixture(scope="module")
def poetry_2_1_pyproject_text(sample_versions) -> str:
    return f"""
    [project]
    name = "project"
    version = "0.1.0"
    description = ""
    authors = []
    readme = "README.md"
    requires-python = ">=3.10"
    dependencies = [
        "pylint (=={sample_versions.pylint})"
    ]

    [tool.poetry]
    packages = [{{include = "project", from = "src"}}]

    [tool.poetry.group.dev.dependencies]
    isort = "{sample_versions.isort}"

    [tool.poetry.group.analysis.dependencies]
    black = "{sample_versions.black}"

    [project.optional-dependencies]
    ruff = [ "ruff (=={sample_versions.ruff})" ]

    [build-system]
    requires = ["poetry-core>=2.0.0,<3.0.0"]
    build-backend = "poetry.core.masonry.api"
    """


@pytest.fixture(scope="module")
def poetry_2_3_pyproject_text(sample_versions) -> str:
    return f"""
    [project]
    name = "project"
    version = "0.1.0"
    description = ""
    authors = []
    readme = "README.md"
    requires-python = ">=3.10"
    dependencies = [
        "pylint (=={sample_versions.pylint})"
    ]

    [tool.poetry]
    packages = [{{include = "project", from = "src"}}]

    [dependency-groups]
    dev = [
        "isort=={sample_versions.isort}",
    ]
    analysis = [
        "black=={sample_versions.black}"
    ]

    [project.optional-dependencies]
    ruff = [ "ruff (=={sample_versions.ruff})" ]

    [build-system]
    requires = ["poetry-core>=2.0.0,<3.0.0"]
    build-backend = "poetry.core.masonry.api"
    """


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
def create_new_poetry_project(
    poetry_path, cwd, project_name, project_path, sample_versions
):
    subprocess.run([poetry_path, "new", project_name], cwd=cwd, check=True)

    commands = [
        [poetry_path, "self", "add", "poetry-plugin-export"],
        [poetry_path, "add", f"pylint=={sample_versions.pylint}"],
        [poetry_path, "add", "--group", "dev", f"isort=={sample_versions.isort}"],
        [poetry_path, "add", "--group", "analysis", f"black=={sample_versions.black}"],
        [poetry_path, "add", f"ruff@{sample_versions.ruff}", "--optional", "ruff"],
    ]
    for cmd in commands:
        subprocess.run(cmd, cwd=project_path, env={}, check=True)
