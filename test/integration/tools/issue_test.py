from unittest.mock import patch

from exasol.toolbox.tools.issue import CLI


class TestListIssues:
    @staticmethod
    def test_with_default(cli_runner):
        result = cli_runner.invoke(CLI, ["list"])

        assert result.exit_code == 0
        assert (
            result.output
            == "blank\nbug\ndocumentation\nfeature\nrefactoring\nsecurity\n"
        )

    @staticmethod
    def test_with_column(cli_runner):
        result = cli_runner.invoke(CLI, ["list", "--columns"])

        assert result.exit_code == 0
        assert result.output == (
            "blank     bug    documentation        feature     refactoring       "
            "security    \n"
        )


def test_show_issue(cli_runner):
    result = cli_runner.invoke(CLI, ["show", "bug"])

    assert result.exit_code == 0
    assert "name: Bug " in result.output


def test_diff_issue(cli_runner, tmp_path):
    # set up with file in tmp_path so bug files are the same
    cli_runner.invoke(CLI, ["install", "bug", str(tmp_path)])

    result = cli_runner.invoke(CLI, ["diff", "bug", str(tmp_path)])

    assert result.exit_code == 0
    # as the files are the same, we expect no difference
    assert result.output.strip() == ""


class TestInstallIssue:
    @staticmethod
    def test_all_issues(cli_runner, tmp_path):
        result = cli_runner.invoke(CLI, ["install", "all", str(tmp_path)])
        all_files = sorted([filepath.name for filepath in tmp_path.iterdir()])

        assert result.exit_code == 0
        assert all_files == [
            "blank.md",
            "bug.md",
            "documentation.md",
            "feature.md",
            "refactoring.md",
            "security.md",
        ]
        assert f"Installed blank in {tmp_path}/blank.md" in result.output

    @staticmethod
    def test_install_twice_no_error(cli_runner, tmp_path):
        cli_runner.invoke(CLI, ["install", "bug", str(tmp_path)])
        result = cli_runner.invoke(CLI, ["install", "bug", str(tmp_path)])
        all_files = sorted([filepath.name for filepath in tmp_path.iterdir()])

        assert result.exit_code == 0
        assert all_files == ["bug.md"]
        assert f"Installed bug in \n{tmp_path}/bug.md" in result.output


class TestUpdateIssue:
    @staticmethod
    def test_when_file_does_not_previously_exist(cli_runner, tmp_path):
        result = cli_runner.invoke(CLI, ["update", "bug", str(tmp_path)])

        assert result.exit_code == 0
        assert result.output.strip() == f"Updated bug in \n{tmp_path}/bug.md"

    @staticmethod
    def test_with_existing_file(cli_runner, tmp_path):
        # set up with file in tmp_path so bug files are the same
        cli_runner.invoke(CLI, ["install", "bug", str(tmp_path)])

        with patch("typer.confirm", return_value=False):
            result = cli_runner.invoke(CLI, ["update", "bug", str(tmp_path)])

        assert result.exit_code == 0
        # files are identical, so no output expected
        assert result.output.strip() == ""
