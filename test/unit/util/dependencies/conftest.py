import os
import subprocess
from enum import Enum

import pytest


class SampleVersions(str, Enum):
    black = "25.1.0"
    isort = "6.0.1"
    pylint = "3.3.7"
    ruff = "0.14.14"


def _path_without_active_virtualenv() -> str:
    path = os.environ.get("PATH", "")
    if not (virtualenv := os.environ.get("VIRTUAL_ENV")):
        return path

    virtualenv_bin = os.path.abspath(os.path.join(virtualenv, "bin"))
    return os.pathsep.join(
        part
        for part in path.split(os.pathsep)
        if os.path.abspath(part) != virtualenv_bin
    )


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
        "pylint (=={sample_versions.pylint.value})"
    ]

    [tool.poetry]
    packages = [{{include = "project", from = "src"}}]

    [tool.poetry.group.dev.dependencies]
    isort = "{sample_versions.isort.value}"

    [tool.poetry.group.analysis.dependencies]
    black = "{sample_versions.black.value}"

    [project.optional-dependencies]
    ruff = [ "ruff (=={sample_versions.ruff.value})" ]

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
        "pylint (=={sample_versions.pylint.value})"
    ]

    [tool.poetry]
    packages = [{{include = "project", from = "src"}}]

    [dependency-groups]
    dev = [
        "isort=={sample_versions.isort.value}",
    ]
    analysis = [
        "black=={sample_versions.black.value}"
    ]

    [project.optional-dependencies]
    ruff = [ "ruff (=={sample_versions.ruff.value})" ]

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
def poetry_env(cwd):
    return {
        "HOME": str(cwd),
        "PATH": _path_without_active_virtualenv(),
        "POETRY_CACHE_DIR": str(cwd / ".cache" / "pypoetry"),
        "POETRY_CONFIG_DIR": str(cwd / ".config" / "pypoetry"),
        "POETRY_DATA_DIR": str(cwd / ".local" / "share" / "pypoetry"),
        "POETRY_VIRTUALENVS_IN_PROJECT": "true",
    }


@pytest.fixture
def isolated_poetry_env(monkeypatch, poetry_env):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.delenv("POETRY_ACTIVE", raising=False)
    for name, value in poetry_env.items():
        monkeypatch.setenv(name, value)


@pytest.fixture(scope="module")
def create_new_poetry_project(
    poetry_path, cwd, project_name, project_path, sample_versions, poetry_env
):
    subprocess.run(
        [poetry_path, "new", "--python=>=3.10", project_name],
        cwd=cwd,
        env=poetry_env,
        check=True,
    )

    commands = [
        [poetry_path, "add", f"pylint=={sample_versions.pylint.value}"],
        [poetry_path, "add", "--group", "dev", f"isort=={sample_versions.isort.value}"],
        [
            poetry_path,
            "add",
            "--group",
            "analysis",
            f"black=={sample_versions.black.value}",
        ],
        [
            poetry_path,
            "add",
            f"ruff@{sample_versions.ruff.value}",
            "--optional",
            "ruff",
        ],
    ]
    for cmd in commands:
        subprocess.run(cmd, cwd=project_path, env=poetry_env, check=True)
