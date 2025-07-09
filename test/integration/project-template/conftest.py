import subprocess

import pytest

from noxconfig import Config


@pytest.fixture(scope="session")
def cwd(tmp_path_factory):
    return tmp_path_factory.mktemp("project_template_test")


@pytest.fixture(scope="session")
def new_project(cwd):
    project_name = "project"
    repo_name = "repo"
    package_name = "package"

    subprocess.run(["pip", "install", "cookiecutter"], capture_output=True, check=True)
    subprocess.run(
        ["cookiecutter", Config.root / "project-template", "-o", cwd, "--no-input",
         f"project_name={project_name}", f"repo_name={repo_name}",
         f"package_name={package_name}", "author_full_name=tester",
         "author_email=test@exasol.com"
         ], capture_output=True, check=True)

    return cwd / repo_name
