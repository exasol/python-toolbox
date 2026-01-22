from unittest.mock import patch

import pytest

from exasol.toolbox.tools.workflow import CLI


class TestListWorkflows:
    @staticmethod
    def test_with_default(cli_runner):
        result = cli_runner.invoke(CLI, ["list"])

        assert result.exit_code == 0
        assert result.output == (
            "build-and-publish\n"
            "cd\n"
            "check-release-tag\n"
            "checks\n"
            "ci\n"
            "gh-pages\n"
            "matrix-all\n"
            "matrix-exasol\n"
            "matrix-python\n"
            "merge-gate\n"
            "pr-merge\n"
            "report\n"
            "slow-checks\n"
        )

    @staticmethod
    def test_with_columns(cli_runner):
        result = cli_runner.invoke(CLI, ["list", "--columns"])

        assert result.exit_code == 0
        assert result.output == (
            "build-and-publish  cd             check-release-tag checks     ci       "
            "gh-pages\n"
            "matrix-all         matrix-exasol  matrix-python     merge-gate pr-merge "
            "report  \n"
            "slow-checks                                                                     \n"
        )


def test_show_workflow(cli_runner):
    result = cli_runner.invoke(CLI, ["show", "checks"])

    assert result.exit_code == 0
    assert "name: Checks " in result.output


@pytest.mark.parametrize(
    "workflow",
    [
        "build-and-publish",
        "cd",
        "check-release-tag",
        "checks",
        "ci",
        "gh-pages",
        "matrix-all",
        "matrix-exasol",
        "matrix-python",
        "merge-gate",
        "pr-merge",
        "report",
        "slow-checks",
    ],
)
def test_diff_workflow(cli_runner, tmp_path, workflow):
    # set up with file in tmp_path so checks files are the same
    cli_runner.invoke(CLI, ["install", workflow, str(tmp_path)])

    result = cli_runner.invoke(CLI, ["diff", workflow, str(tmp_path)])

    assert result.exit_code == 0
    # as the files are the same, we expect no difference
    assert result.output.strip() == ""


class TestInstallWorkflow:
    @staticmethod
    def test_all_workflows(cli_runner, tmp_path):
        result = cli_runner.invoke(CLI, ["install", "all", str(tmp_path)])
        all_files = sorted([filepath.name for filepath in tmp_path.iterdir()])

        assert result.exit_code == 0
        assert all_files == [
            "build-and-publish.yml",
            "cd.yml",
            "check-release-tag.yml",
            "checks.yml",
            "ci.yml",
            "gh-pages.yml",
            "matrix-all.yml",
            "matrix-exasol.yml",
            "matrix-python.yml",
            "merge-gate.yml",
            "pr-merge.yml",
            "report.yml",
            "slow-checks.yml",
        ]
        assert (
            f"Installed build-and-publish in \n{tmp_path}/build-and-publish.yml"
            in result.output
        )

    @staticmethod
    def test_install_twice_no_error(cli_runner, tmp_path):
        cli_runner.invoke(CLI, ["install", "checks", str(tmp_path)])
        result = cli_runner.invoke(CLI, ["install", "checks", str(tmp_path)])
        all_files = sorted([filepath.name for filepath in tmp_path.iterdir()])

        assert result.exit_code == 0
        assert all_files == ["checks.yml"]
        assert f"Installed checks in \n{tmp_path}/checks.yml" in result.output


class TestUpdateWorkflow:
    @staticmethod
    def test_when_file_does_not_previously_exist(cli_runner, tmp_path):
        result = cli_runner.invoke(CLI, ["update", "checks", str(tmp_path)])

        assert result.exit_code == 0
        assert result.output.strip() == f"Updated checks in \n{tmp_path}/checks.yml"

    @staticmethod
    def test_with_existing_file(cli_runner, tmp_path):
        # set up with file in tmp_path so checks files are the same
        cli_runner.invoke(CLI, ["install", "checks", str(tmp_path)])

        with patch("typer.confirm", return_value=False):
            result = cli_runner.invoke(CLI, ["update", "checks", str(tmp_path)])

        assert result.exit_code == 0
        # files are identical, so no output expected
        assert result.output.strip() == ""
