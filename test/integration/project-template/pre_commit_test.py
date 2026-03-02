import pytest


@pytest.fixture(scope="module")
def pre_commit(run_command, new_project, poetry_path):
    run_command(["git", "init"])
    run_command([poetry_path, "run", "--", "pre-commit", "install"])


class TestPreCommitConfig:
    @staticmethod
    def _command(poetry_path: str, stage: str) -> list[str]:
        return [
            poetry_path,
            "run",
            "--",
            "pre-commit",
            "run",
            "--hook-stage",
            stage,
            "--files",
            "exasol/package/version.py",
        ]

    def test_stage_pre_commit(self, pre_commit, poetry_path, run_command):
        command = self._command(poetry_path, "pre-commit")
        output = run_command(command, check=False)

        assert "Failed" not in output.stdout
        assert "Passed" in output.stdout
        assert output.returncode == 0

    def test_stage_pre_push(self, pre_commit, poetry_path, run_command):
        command = self._command(poetry_path, "pre-push")
        output = run_command(command, check=False)

        assert "Failed" not in output.stdout
        assert "Passed" in output.stdout
        assert output.returncode == 0
