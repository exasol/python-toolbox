import json
from unittest.mock import patch

from exasol.toolbox.tools.security import (
    CLI,
    CVE_CLI,
    Filter,
    Format,
)

JSON_RESULTS = {
    "results": [
        {
            "code": '555                 subprocess.check_call(\n556                     config.smv_postbuild_command, cwd=current_cwd, shell=True\n557                 )\n558                 if config.smv_postbuild_export_pattern != "":\n559                     matches = find_matching_files_and_dirs(\n',
            "col_offset": 16,
            "end_col_offset": 17,
            "filename": "exasol/toolbox/sphinx/multiversion/main.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
                "id": 78,
                "link": "https://cwe.mitre.org/data/definitions/78.html",
            },
            "issue_severity": "HIGH",
            "issue_text": "subprocess call with shell=True identified, security issue.",
            "line_number": 556,
            "line_range": [555, 556, 557],
            "more_info": "https://bandit.readthedocs.io/en/1.7.10/plugins/b602_subprocess_popen_with_shell_equals_true.html",
            "test_id": "B602",
            "test_name": "subprocess_popen_with_shell_equals_true",
        },
        {
            "code": "156         )\n157         subprocess.check_call(cmd, cwd=gitroot, stdout=fp)\n158         fp.seek(0)\n",
            "col_offset": 8,
            "end_col_offset": 58,
            "filename": "exasol/toolbox/sphinx/multiversion/git.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
                "id": 78,
                "link": "https://cwe.mitre.org/data/definitions/78.html",
            },
            "issue_severity": "LOW",
            "issue_text": "subprocess call - check for execution of untrusted input.",
            "line_number": 157,
            "line_range": [157],
            "more_info": "https://bandit.readthedocs.io/en/1.7.10/plugins/b603_subprocess_without_shell_equals_true.html",
            "test_id": "B603",
            "test_name": "subprocess_without_shell_equals_true",
        },
        {
            "code": "159         with tarfile.TarFile(fileobj=fp) as tarfp:\n160             tarfp.extractall(dst)\n",
            "col_offset": 12,
            "end_col_offset": 33,
            "filename": "exasol/toolbox/sphinx/multiversion/git.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
                "id": 22,
                "link": "https://cwe.mitre.org/data/definitions/22.html",
            },
            "issue_severity": "HIGH",
            "issue_text": "tarfile.extractall used without any validation. Please check and discard dangerous members.",
            "line_number": 160,
            "line_range": [160],
            "more_info": "https://bandit.readthedocs.io/en/1.7.10/plugins/b202_tarfile_unsafe_members.html",
            "test_id": "B202",
            "test_name": "tarfile_unsafe_members",
        },
    ]
}


class TestConvert:
    @staticmethod
    def test_with_filled_file(cli_runner, tmp_path, sample_maven_vulnerabilities):
        json_path = tmp_path / "input.json"
        json_path.write_text(sample_maven_vulnerabilities.report_json)

        result = cli_runner.invoke(
            CVE_CLI, ["convert", Format.Maven.value, str(json_path)]
        )

        assert result.exit_code == 0
        assert result.output.strip() == sample_maven_vulnerabilities.issues_json


class TestFilter:
    @staticmethod
    def test_without_existing_github_issue_passes_through(
        cli_runner, tmp_path, sample_maven_vulnerabilities
    ):
        json_path = tmp_path / "input.json"
        json_path.write_text(sample_maven_vulnerabilities.issues_json)

        result = cli_runner.invoke(
            CVE_CLI, ["filter", Filter.GitHubIssues.value, str(json_path)]
        )

        assert result.exit_code == 0
        assert result.output.strip() == sample_maven_vulnerabilities.issues_json

    @staticmethod
    def test_with_existing_github_issue_is_filtered_out(
        cli_runner, tmp_path, sample_maven_vulnerabilities
    ):
        json_path = tmp_path / "input.json"
        json_path.write_text(sample_maven_vulnerabilities.issues_json)

        with patch(
            "exasol.toolbox.tools.security.gh_security_issues",
            return_value=sample_maven_vulnerabilities.gh_security_issues,
        ):
            result = cli_runner.invoke(
                CVE_CLI, ["filter", Filter.GitHubIssues.value, str(json_path)]
            )

        assert result.exit_code == 0
        assert result.output.strip() == ""


class TestCreate:
    @staticmethod
    def test_works_as_expected_with_mocked_create_security_issue(
        cli_runner, tmp_path, sample_maven_vulnerabilities
    ):
        json_path = tmp_path / "input.json"
        json_path.write_text(sample_maven_vulnerabilities.issues_json)

        with patch(
            "exasol.toolbox.tools.security.create_security_issue",
            return_value=("", sample_maven_vulnerabilities.github_issue_url),
        ):
            result = cli_runner.invoke(CVE_CLI, ["create", str(json_path)])

        assert result.exit_code == 0
        assert result.output.strip() == sample_maven_vulnerabilities.create_issues_json


class TestJsonIssueToMarkdown:
    @staticmethod
    def test_with_filled_file(cli_runner, tmp_path):
        json_path = tmp_path / "test.json"
        json_path.write_text(json.dumps(JSON_RESULTS))

        result = cli_runner.invoke(CLI, ["pretty-print", str(json_path)])

        assert result.exit_code == 0
        assert result.output.strip() == (
            "# Security\n\n"
            "|File|line/<br>column|Cwe|Test ID|Details|\n"
            "|---|:-:|:-:|:-:|---|\n"
            "|exasol/toolbox/sphinx/multiversion/git.py|line: 160<br>column: "
            "12|22|B202|https://bandit.readthedocs.io/en/1.7.10/plugins/b202_tarfile_unsafe_members.html "
            ",<br>https://cwe.mitre.org/data/definitions/22.html |\n"
            "|exasol/toolbox/sphinx/multiversion/git.py|line: 157<br>column: "
            "8|78|B603|https://bandit.readthedocs.io/en/1.7.10/plugins/b603_subprocess_without_shell_equals_true.html "
            ",<br>https://cwe.mitre.org/data/definitions/78.html |\n"
            "|exasol/toolbox/sphinx/multiversion/main.py|line: 556<br>column: "
            "16|78|B602|https://bandit.readthedocs.io/en/1.7.10/plugins/b602_subprocess_popen_with_shell_equals_true.html "
            ",<br>https://cwe.mitre.org/data/definitions/78.html |"
        )

    @staticmethod
    def test_with_empty_file(cli_runner, tmp_path):
        contents = {"result": []}
        json_path = tmp_path / "test.json"
        json_path.write_text(json.dumps(contents))

        result = cli_runner.invoke(CLI, ["pretty-print", str(json_path)])

        assert result.exit_code == 0
        assert result.output.strip() == (
            "# Security\n\n"
            "|File|line/<br>column|Cwe|Test ID|Details|\n"
            "|---|:-:|:-:|:-:|---|"
        )
