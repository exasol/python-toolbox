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
