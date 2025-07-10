from typing import Union


class TestSpecificNoxTasks:
    """
    Within the PTB, we have nox tasks that are inherently dependent upon other ones
    working & delivering specific results to other ones. These relationships
    are tested within the GitHub workflows in a distributed manner, which means
    that sometimes, when issues are experienced, that it can be quite cumbersome
    to determine where the issue arose.

    Additionally, the project-template itself is not tested in these workflows.
    So the tests included here are meant to cover common pain points to ensure
    both the relationships between nox tasks and ensuring that the project-template
    passes CI tests when a new project is created from it.
    """
    @staticmethod
    def _command(poetry_path: str, task: str, add_ons: Union[list[str]|None]=None) -> list[str]:
        base = [poetry_path, "run", "--", "nox", "-s", task]
        if add_ons:
            base = base + ["--"] + add_ons
        return base

    def test_lint_code(self, poetry_path, run_command):
        command = self._command(poetry_path, "lint:code")
        output = run_command(command, check=False)

        assert output.returncode == 0

    def test_artifact_validate(self, poetry_path, run_command):
        # preparation steps
        lint_code = self._command(poetry_path, "lint:code")
        run_command(lint_code)
        lint_security = self._command(poetry_path, "lint:security")
        run_command(lint_security)
        test_unit = self._command(poetry_path, "test:unit",["--coverage"])
        run_command(test_unit)
        test_integration = self._command(poetry_path, "test:integration",["--coverage"])
        run_command(test_integration)
        # we skip uploading & downloading artifacts, so the coverage combination is
        # skipped here from `artifacts:copy`

        artifacts_validate = self._command(poetry_path, "artifacts:validate")
        output = run_command(artifacts_validate, check=False)

        assert output.returncode == 0
