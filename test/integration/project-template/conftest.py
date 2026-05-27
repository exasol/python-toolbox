import logging
import subprocess
from pathlib import Path

import pytest

from noxconfig import PROJECT_CONFIG

LOG = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def cwd(tmp_path_factory):
    return tmp_path_factory.mktemp("project_template_test")


@pytest.fixture(scope="session")
def package_name():
    return "package"


@pytest.fixture(scope="session")
def ptb_wheel_dir(cwd):
    return cwd / "ptb-wheel"


@pytest.fixture(scope="session")
def ptb_wheel(poetry_path, ptb_wheel_dir):
    ptb_wheel_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [poetry_path, "build", "--output", ptb_wheel_dir],
        cwd=PROJECT_CONFIG.root_path,
        check=True,
    )
    return min(ptb_wheel_dir.glob("exasol_toolbox-*.whl"))


@pytest.fixture(scope="session", autouse=True)
def new_project(cwd, package_name):
    project_name = "project"
    repo_name = "repo"
    project_path = cwd / repo_name

    subprocess.run(["mkdir", "-p", project_path])
    subprocess.run(["git", "init"], cwd=project_path)

    subprocess.run(
        [
            "cookiecutter",
            PROJECT_CONFIG.root_path / "project-template",
            "-o",
            cwd,
            "--no-input",
            "--overwrite-if-exists",
            f"project_name={project_name}",
            f"repo_name={repo_name}",
            f"package_name={package_name}",
        ],
        capture_output=True,
        check=True,
    )
    return cwd / repo_name


@pytest.fixture(scope="session", autouse=True)
def poetry_install(run_command, poetry_path, ptb_wheel):
    # The tests want to verify the current branch of the PTB incl. its cookiecutter
    # template before releasing the PTB. We install a built wheel from the checked-out
    # PTB instead of using an editable dependency so the fixture mirrors release-like
    # installation behavior.
    run_command([poetry_path, "install"])
    run_command(
        [
            poetry_path,
            "run",
            "--",
            "pip",
            "install",
            "--no-deps",
            "--force-reinstall",
            str(ptb_wheel),
        ]
    )


@pytest.fixture(scope="session")
def git_path() -> str:
    result = subprocess.run(["which", "git"], capture_output=True, text=True)
    git_path = result.stdout.strip()
    return git_path


@pytest.fixture(scope="session")
def run_command(poetry_path, git_path, new_project):
    """
    Run subprocess command with captured output and a limited environment (env).

    We restrict the environment as different systems & tools (i.e. PyCharm) include
    environment variables which may supersede the ones provided here. In such cases,
    this can lead to a breaking alteration in the PTB poetry environment. Thus,
    we provide the minimum information needed to execute the pre-commit command.
    """

    def _run_command_fixture(command, **kwargs):
        cwd = new_project
        env = {"PATH": f"{Path(git_path).parent}:{Path(poetry_path).parent}"}
        defaults = {
            "capture_output": True,
            "cwd": cwd,
            "env": env,
            "text": True,
        }
        config = {**defaults, **kwargs, "check": False}
        p = subprocess.run(command, **config)
        if p.returncode != 0:

            def text(stream) -> str:
                return "" if stream is None else stream.strip()

            message = (
                f"subprocess.run() returned exit code: {p.returncode}"
                f"\ncommand: {' '.join(command)}"
                f"\nstdout: {text(p.stdout)}"
                f"\nstderr: {text(p.stderr)}"
                f"\ncwd: {cwd}"
                f"\nenv: {env}"
            )
            LOG.warning(message)
            if kwargs.get("check", True):
                raise subprocess.CalledProcessError(
                    p.returncode,
                    command,
                    output=p.stdout,
                    stderr=p.stderr,
                )
        return p

    return _run_command_fixture
