

class TestSpecificNoxTasks:
    @staticmethod
    def _command(poetry_path: str, task: str) -> list[str]:
        return [poetry_path, "run", "--", "nox", "-s", task]

    def test_lint_code(self, poetry_path, run_command):
        command = self._command(poetry_path, "lint:code")
        output = run_command(command, check=False)
        assert output.returncode == 0
