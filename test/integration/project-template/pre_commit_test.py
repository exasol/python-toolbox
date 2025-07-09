import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def poetry_path() -> str:
    result = subprocess.run(["which", "poetry"], capture_output=True, text=True)
    poetry_path = result.stdout.strip()
    return poetry_path


@pytest.fixture(scope="module")
def git_path() -> str:
    result = subprocess.run(["which", "git"], capture_output=True, text=True)
    git_path = result.stdout.strip()
    return git_path


@pytest.fixture(scope="module")
def run_command(poetry_path, git_path, new_project):
    def _run_command_fixture(command, **kwargs):
        defaults = {
            "capture_output": True,
            "check": True,
            "cwd": new_project,
            "env": {"PATH": f"{Path(git_path).parent}:{Path(poetry_path).parent}"},
            "text": True,

        }
        config = {**defaults, **kwargs}

        return subprocess.run(command, **config)

    return _run_command_fixture


@pytest.fixture(scope="module")
def pre_commit(run_command, new_project, poetry_path):
    run_command(command=["git", "init"])
    run_command([poetry_path, "add", "pre-commit"])
    run_command([poetry_path, "install"])
    run_command([poetry_path, "run", "--", "pre-commit", "install"])


class TestPreCommitConfig:
    @staticmethod
    def _command(poetry_path: str, stage: str) -> list[str]:
        return [poetry_path, "run", "--", "pre-commit", "run", "--hook-stage", stage,
                "--files",
                "exasol/package/version.py"]

    def test_stage_pre_commit(self, pre_commit, poetry_path, run_command):
        command = self._command(poetry_path, "pre-commit")
        output = run_command(command=command, check=False)

        assert "Failed" not in output.stdout
        assert "Passed" in output.stdout
        assert output.returncode == 0

    def test_stage_pre_push(self, pre_commit, poetry_path, run_command):
        command = self._command(poetry_path, "pre-push")
        output = run_command(command=command, check=False)

        assert "Failed" not in output.stdout
        assert "Passed" in output.stdout
        assert output.returncode == 0
