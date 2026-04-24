import pytest


@pytest.fixture(scope="module")
def poetry_2_1_pyproject_text() -> str:
    return """
    [project]
    name = "project"
    version = "0.1.0"
    description = ""
    authors = []
    readme = "README.md"
    requires-python = ">=3.10"
    dependencies = [
        "pylint (==3.3.7)"
    ]

    [tool.poetry]
    packages = [{include = "project", from = "src"}]

    [tool.poetry.group.dev.dependencies]
    isort = "6.0.1"

    [tool.poetry.group.analysis.dependencies]
    black = "25.1.0"

    [project.optional-dependencies]
    ruff = [ "ruff (==0.14.14)" ]

    [build-system]
    requires = ["poetry-core>=2.0.0,<3.0.0"]
    build-backend = "poetry.core.masonry.api"
    """


@pytest.fixture(scope="module")
def poetry_2_3_pyproject_text() -> str:
    return """
    [project]
    name = "project"
    version = "0.1.0"
    description = ""
    authors = []
    readme = "README.md"
    requires-python = ">=3.10"
    dependencies = [
        "pylint (==3.3.7)"
    ]

    [tool.poetry]
    packages = [{include = "project", from = "src"}]

    [dependency-groups]
    dev = [
        "isort==6.0.1",
    ]
    analysis = [
        "black==25.1.0"
    ]

    [project.optional-dependencies]
    ruff = [ "ruff (==0.14.14)" ]

    [build-system]
    requires = ["poetry-core>=2.0.0,<3.0.0"]
    build-backend = "poetry.core.masonry.api"
    """
