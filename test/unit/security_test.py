import json
import os
import pathlib
import subprocess
from contextlib import contextmanager
from inspect import cleandoc
from unittest import mock

import pytest

from exasol.toolbox.tools import security


@contextmanager
def empty_path():
    """Make sure the PATH environment variable is empty."""
    old_path = os.environ["PATH"]
    os.environ["PATH"] = ""
    yield
    os.environ["PATH"] = old_path


class TestCreateSecurityIssue:
    @pytest.mark.parametrize(
        "expected,issue",
        [
            (
                "CVE-2023-39410: pkg:maven/fr.turri/aXMLRPC@1.13.0",
                security.Issue(
                    cve="CVE-2023-39410",
                    cwe="None",
                    description="None",
                    coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
                    references=tuple(),
                ),
            )
        ],
    )
    def test_security_issue_title_template(self, expected, issue):
        actual = security.security_issue_title(issue)
        assert actual == expected

    @pytest.mark.parametrize(
        "expected,issue",
        [
            (
                cleandoc(
                    """
                    ## Summary
                    Random Multiline
                    Description
                    ;)

                    CVE: CVE-2023-39410
                    CWE: CWE-XYZ

                    ## References
                    - https://www.example.com
                    - https://www.foobar.com
                    """
                ),
                security.Issue(
                    cve="CVE-2023-39410",
                    cwe="CWE-XYZ",
                    description="Random Multiline\nDescription\n;)",
                    coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
                    references=("https://www.example.com", "https://www.foobar.com"),
                ),
            )
        ],
    )
    def test_security_issue_body_template(self, expected, issue):
        actual = security.security_issue_body(issue)
        assert actual == expected

    def test_gh_cli_is_not_available(self):
        with empty_path():
            with pytest.raises(FileNotFoundError) as exec_info:
                set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = "Command 'gh' not found. Please make sure you have installed the github cli."

        assert actual == expected

    @mock.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd=[
                "gh",
                "issue",
                "create",
                "--label",
                "security",
                "--title",
                "<title>",
                "--body",
                "<body>",
            ],
        ),
    )
    def test_gh_cli_failed(self, _):
        with pytest.raises(subprocess.CalledProcessError) as exec_info:
            set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = str(
            subprocess.CalledProcessError(
                returncode=1,
                cmd=[
                    "gh",
                    "issue",
                    "create",
                    "--label",
                    "security",
                    "--title",
                    "<title>",
                    "--body",
                    "<body>",
                ],
            )
        )
        assert actual == expected

    @mock.patch("subprocess.run")
    def test_query_gh_security_issues(self, run_mock):
        result = mock.MagicMock(subprocess.CompletedProcess)
        result.returncode = 0
        result.stdout = b"https://github.com/exasol/some-project/issues/16"
        result.stderr = b"Creating Issue"
        run_mock.return_value = result

        issues = security.Issue(
            cve="CVE-2023-39410",
            cwe="None",
            description="None",
            coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
            references=tuple(),
        )

        expected = (
            "Creating Issue",
            "https://github.com/exasol/some-project/issues/16",
        )
        actual = security.create_security_issue(issues)
        assert actual == expected


class TestGhSecurityIssues:
    def test_gh_cli_is_not_available(self):
        with empty_path():
            with pytest.raises(FileNotFoundError) as exec_info:
                set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = "Command 'gh' not found. Please make sure you have installed the github cli."

        assert actual == expected

    @mock.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd=[
                "gh",
                "issue",
                "list",
                "--label",
                "security",
                "--search",
                "CVE",
                "--json",
                "id,title",
                "1000",
            ],
        ),
    )
    def test_gh_cli_failed(self, _):
        with pytest.raises(subprocess.CalledProcessError) as exec_info:
            set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = str(
            subprocess.CalledProcessError(
                returncode=1,
                cmd=[
                    "gh",
                    "issue",
                    "list",
                    "--label",
                    "security",
                    "--search",
                    "CVE",
                    "--json",
                    "id,title",
                    "1000",
                ],
            )
        )
        assert actual == expected

    @mock.patch("subprocess.run")
    def test_query_gh_security_issues(self, run_mock):
        result = mock.MagicMock(subprocess.CompletedProcess)
        result.returncode = 0
        result.stdout = (
            b'[{"id":"I_kwDOIRnUks5zutba","title":"\xf0\x9f\x90\x9e CVE-2023-41105: Fix build scripts "},'
            b'{"id":"I_kwDOIRnUks5clFdR","title":"\xf0\x9f\x90\x9e CVE-2023-40217: Version check issues"}]\n'
        )
        run_mock.return_value = result

        expected = {
            ("I_kwDOIRnUks5zutba", "CVE-2023-41105"),
            ("I_kwDOIRnUks5clFdR", "CVE-2023-40217"),
        }
        actual = set(security.gh_security_issues())
        assert actual == expected


class TestConvertMavenInput:
    @staticmethod
    def test_with_filled_input(sample_maven_vulnerabilities):
        actual = set(security.from_maven(sample_maven_vulnerabilities.report_json))
        assert actual == sample_maven_vulnerabilities.issues

    @staticmethod
    def test_with_empty_input():
        actual = set(security.from_maven("{}"))
        assert len(actual) == 0


def test_format_jsonl():
    issue = security.Issue(
        coordinates="coordinates",
        cve="cve",
        cwe="cwe",
        description="description",
        references=(),
    )
    expected = json.dumps(
        {
            "cve": "cve",
            "cwe": "cwe",
            "description": "description",
            "coordinates": "coordinates",
            "references": [],
            "issue_url": "my_issue_url",
        }
    )
    actual = security.format_jsonl("my_issue_url", issue)
    assert actual == expected


def test_format_jsonl_removes_newline():
    issue = security.Issue(
        coordinates="coordinates",
        cve="cve",
        cwe="cwe",
        description="description",
        references=(),
    )
    expected = json.dumps(
        {
            "cve": "cve",
            "cwe": "cwe",
            "description": "description",
            "coordinates": "coordinates",
            "references": [],
            "issue_url": "my_issue_url",
        }
    )
    actual = security.format_jsonl("my_issue_url\n", issue)
    assert actual == expected


@pytest.mark.parametrize(
    "json_input,expected",
    [
        (
            {
                "results": [
                    {
                        "code": "1 import subprocess\\n2 from typing import Iterable\\n3 \\n",
                        "col_offset": 12,
                        "end_col_offset": 17,
                        "filename": "/home/test/python-toolbox/exasol/toolbox/git.py",
                        "issue_confidence": "HIGH",
                        "issue_cwe": {
                            "id": 78,
                            "link": "https://cwe.mitre.org/data/definitions/78.html",
                        },
                        "issue_severity": "LOW",
                        "issue_text": "Consider possible security implications associated with the subprocess module.",
                        "line_number": 53,
                        "line_range": [1],
                        "more_info": "https://bandit.readthedocs.io/en/1.7.10/blacklists/blacklist_imports.html#b404-import-subprocess",
                        "test_id": "B404",
                        "test_name": "blacklist",
                    }
                ]
            },
            {
                "file_name": "exasol/toolbox/git.py",
                "line": 53,
                "column": 12,
                "cwe": "78",
                "test_id": "B404",
                "description": "Consider possible security implications associated with the subprocess module.",
                "references": (
                    "https://bandit.readthedocs.io/en/1.7.10/blacklists/blacklist_imports.html#b404-import-subprocess",
                    "https://cwe.mitre.org/data/definitions/78.html",
                ),
            },
        )
    ],
)
def test_from_json(json_input, expected):
    json_file = json.dumps(json_input)
    actual = security.from_json(json_file, pathlib.Path("/home/test/python-toolbox"))
    expected_issue = security.SecurityIssue(
        file_name=expected["file_name"],
        line=expected["line"],
        column=expected["column"],
        cwe=expected["cwe"],
        test_id=expected["test_id"],
        description=expected["description"],
        references=expected["references"],
    )
    assert list(actual) == [expected_issue]


@pytest.mark.parametrize(
    "reference, expected",
    [
        pytest.param(
            "CVE-2025-27516",
            (["CVE-2025-27516"], []),
            id="CVE_identified_with_link",
        ),
        pytest.param(
            "CWE-611",
            ([], ["CWE-611"]),
            id="CWE_identified_with_link",
        ),
        pytest.param(
            "GHSA-cpwx-vrp4-4pq7",
            ([], []),
            id="GHSA_link",
        ),
        pytest.param(
            "PYSEC-2025-9",
            ([], []),
            id="PYSEC_link",
        ),
    ],
)
def test_identify_pypi_references(reference: str, expected):
    actual = security.identify_pypi_references([reference])
    assert actual == expected


class TestFromPipAudit:
    @staticmethod
    def test_no_vulnerability_returns_empty_list():
        actual = set(security.from_pip_audit("{}"))
        assert actual == set()

    @staticmethod
    def test_convert_vulnerability_to_issue(sample_vulnerability):
        actual = next(
            security.from_pip_audit(sample_vulnerability.nox_dependencies_audit)
        )
        assert actual == sample_vulnerability.security_issue
