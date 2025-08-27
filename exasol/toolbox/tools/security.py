"""This module contains security related CLI tools and code"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections.abc import (
    Generator,
    Iterable,
)
from dataclasses import (
    asdict,
    dataclass,
)
from enum import Enum
from functools import partial
from inspect import cleandoc
from pathlib import Path
from typing import Optional

import typer

stdout = print
stderr = partial(print, file=sys.stderr)


# Note: In the long term we may want to adapt the official CVE json schema
# https://github.com/CVEProject/cve-schema/blob/master/schema/v5.0/CVE_JSON_5.0_schema.json
@dataclass(frozen=True)
class Issue:
    cve: str
    cwe: str
    description: str
    coordinates: str
    references: tuple


def _issues(input) -> Generator[Issue]:
    lines = (l for l in input if l.strip() != "")
    for line in lines:
        obj = json.loads(line)
        yield Issue(**obj)


def _issues_as_json_str(issues):
    for issue in issues:
        issue = asdict(issue)
        yield json.dumps(issue)


def gh_security_issues() -> Generator[tuple[str, str]]:
    """
    Yields issue-id, cve-id pairs for all (closed, open) issues associated with CVEs

    Return:
        A generator which yields tuples of (id,title).

    Raises:
        subprocess.CalledProcessError: If the underlying command fails.
    """
    # fmt: off
    command = [
        "gh", "issue", "list",
        "--label", "security",
        "--search", "CVE",
        "--json", "id,title",
        "--limit", "1000",
    ]
    # fmt: on
    try:
        result = subprocess.run(command, check=True, capture_output=True)
    except FileNotFoundError as ex:
        msg = "Command 'gh' not found. Please make sure you have installed the github cli."
        raise FileNotFoundError(msg) from ex
    except subprocess.CalledProcessError as ex:
        stderr(f"{ex}")
        raise ex

    cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
    issues = json.loads(result.stdout.decode("utf-8"))
    issues = (
        (issue["id"], cve_pattern.search(issue["title"]).group())  # type: ignore
        for issue in issues
        if cve_pattern.search(issue["title"])
    )
    return issues


def from_maven(report: str) -> Iterable[Issue]:
    # Note: Consider adding warnings if there is the same cve with multiple coordinates
    report = json.loads(report)
    dependencies = report.get("vulnerable", {})  # type: ignore
    for dependency_name, dependency in dependencies.items():  # type: ignore
        for v in dependency["vulnerabilities"]:  # type: ignore
            references = [v["reference"]] + v["externalReferences"]
            yield Issue(
                cve=v["cve"],
                cwe=v["cwe"],
                description=v["description"],
                coordinates=dependency_name,
                references=tuple(references),
            )


class VulnerabilitySource(str, Enum):
    CVE = "CVE"
    CWE = "CWE"
    GHSA = "GHSA"
    PYSEC = "PYSEC"

    @classmethod
    def from_prefix(cls, name: str) -> VulnerabilitySource | None:
        for el in cls:
            if name.upper().startswith(el.value):
                return el
        return None

    def get_link(self, package: str, vuln_id: str) -> str:
        if self == VulnerabilitySource.CWE:
            cwe_id = vuln_id.upper().replace(f"{VulnerabilitySource.CWE.value}-", "")
            return f"https://cwe.mitre.org/data/definitions/{cwe_id}.html"

        map_link = {
            VulnerabilitySource.CVE: "https://nvd.nist.gov/vuln/detail/{vuln_id}",
            VulnerabilitySource.GHSA: "https://github.com/advisories/{vuln_id}",
            VulnerabilitySource.PYSEC: "https://github.com/pypa/advisory-database/blob/main/vulns/{package}/{vuln_id}.yaml",
        }
        return map_link[self].format(package=package, vuln_id=vuln_id)


def identify_pypi_references(
    references: list[str], package_name: str
) -> tuple[list[str], list[str], list[str]]:
    refs: dict = {k: [] for k in VulnerabilitySource}
    links = []
    for reference in references:
        if source := VulnerabilitySource.from_prefix(reference.upper()):
            refs[source].append(reference)
            links.append(source.get_link(package=package_name, vuln_id=reference))
    return (
        refs[VulnerabilitySource.CVE],
        refs[VulnerabilitySource.CWE],
        links,
    )


def from_pip_audit(report: str) -> Iterable[Issue]:
    """
    Transforms the JSON output from `nox -s dependency:audit` into an iterable of
    `security.Issue` objects.

    This does not gracefully handle scenarios where:
     - a CVE is not initially associated with the vulnerability; however, the assumption
     is that such vulnerabilities will later be associated with a CVE.
     - the same vulnerability ID (CVE, PYSEC, GHSA, etc.) is present across
     multiple coordinates.

    Input as string:
        [
          {
            "name": "jinja2",
            "version": "3.1.5",
            "refs": [
              "GHSA-cpwx-vrp4-4pq7",
              "CVE-2025-27516"
            ],
            "description": "An oversight ..."
          }
        ]


    Args:
        report:
            the JSON output of `nox -s dependency:audit` provided as a str
    """
    vulnerabilities = json.loads(report)

    for vulnerability in vulnerabilities:
        cves, cwes, links = identify_pypi_references(
            references=vulnerability["refs"], package_name=vulnerability["name"]
        )
        if cves:
            yield Issue(
                cve=sorted(cves)[0],
                cwe="None" if not cwes else ", ".join(cwes),
                description=vulnerability["description"],
                coordinates=f"{vulnerability['name']}:{vulnerability['version']}",
                references=tuple(links),
            )


@dataclass(frozen=True)
class SecurityIssue:
    file_name: str
    line: int
    column: int
    cwe: str
    test_id: str
    description: str
    references: tuple


def from_json(report_str: str, prefix: Path) -> Iterable[SecurityIssue]:
    report = json.loads(report_str)
    issues = report.get("results", {})
    for issue in issues:
        references = []
        if issue["more_info"]:
            references.append(issue["more_info"])
        if issue.get("issue_cwe", {}).get("link", None):
            references.append(issue["issue_cwe"]["link"])
        yield SecurityIssue(
            file_name=issue["filename"].replace(str(prefix) + "/", ""),
            line=issue["line_number"],
            column=issue["col_offset"],
            cwe=str(issue["issue_cwe"].get("id", "")),
            test_id=issue["test_id"],
            description=issue["issue_text"],
            references=tuple(references),
        )


def issues_to_markdown(issues: Iterable[SecurityIssue]) -> str:
    template = cleandoc(
        """
        {header}{rows}
    """
    )

    def _header():
        header = "# Security\n\n"
        header += "|File|line/<br>column|Cwe|Test ID|Details|\n"
        header += "|---|:-:|:-:|:-:|---|\n"
        return header

    def _row(issue):
        row = "|" + issue.file_name + "|"
        row += f"line: {issue.line}<br>column: {issue.column}|"
        row += issue.cwe + "|"
        row += issue.test_id + "|"
        for element in issue.references:
            row += element + " ,<br>"
        row = row[:-5] + "|"
        return row

    return template.format(header=_header(), rows="\n".join(_row(i) for i in issues))


def security_issue_title(issue: Issue) -> str:
    return f"{issue.cve}: {issue.coordinates}"


def security_issue_body(issue: Issue) -> str:
    def as_markdown_listing(elements: Iterable[str]):
        return "\n".join(f"- {element}" for element in elements)

    body = cleandoc(
        """
        ## Summary
        {description}

        CVE: {cve}
        CWE: {cwe}

        ## References
        {references}
        """
    )
    return body.format(
        cve=issue.cve,
        cwe=issue.cwe,
        description=issue.description,
        references=as_markdown_listing(issue.references),
    )


def create_security_issue(
    issue: Issue, project: Optional[str] = None
) -> tuple[str, str]:
    # fmt: off
    command = [
        "gh", "issue", "create",
        "--label", "security",
        "--title", security_issue_title(issue),
        "--body", security_issue_body(issue),
    ]
    if project:
        command.extend(['--project', project])
    # fmt: on
    try:
        result = subprocess.run(command, check=True, capture_output=True)
    except FileNotFoundError as ex:
        msg = "Command 'gh' not found. Please make sure you have installed the github cli."
        raise FileNotFoundError(msg) from ex
    except subprocess.CalledProcessError as ex:
        stderr(f"{ex}")
        raise ex

    std_err = result.stderr.decode("utf-8")
    std_out = result.stdout.decode("utf-8")

    return std_err, std_out


CLI = typer.Typer()
CVE_CLI = typer.Typer()
CLI.add_typer(CVE_CLI, name="cve", help="Work with CVE's")


class Format(str, Enum):
    Maven = "maven"
    PipAudit = "pip-audit"


# pylint: disable=redefined-builtin
@CVE_CLI.command(name="convert")
def convert(
    format: Format = typer.Argument(..., help="input format to be converted."),
    input_file: typer.FileText = typer.Argument(
        default="-", mode="r", help="input file which shall be converted"
    ),
) -> None:
    """
    Convert a language or tool specific security report into a list of cve's in the jsonl format

    Output:
    { "cve": "<cve-id>", "cwe": "<cwe-id>", "description": "<multiline string>", "coordinates": "<string>", "references": ["<url>", "<url>", ...] }
    """

    def _maven(infile):
        issues = from_maven(infile.read())
        for issue in _issues_as_json_str(issues):
            stdout(issue)
        raise typer.Exit(code=0)

    def _pip_audit(infile):
        issues = from_pip_audit(infile.read())
        for issue in _issues_as_json_str(issues):
            stdout(issue)
        raise typer.Exit(code=0)

    actions = {Format.Maven: _maven, Format.PipAudit: _pip_audit}
    action = actions[format]
    action(input_file)


class Filter(str, Enum):
    GitHubIssues = "github-issues"
    PassThrough = "pass-through"


# pylint: disable=redefined-builtin
@CVE_CLI.command(name="filter")
def filter(
    type: Filter = typer.Argument(help="filter type to apply"),
    input_file: typer.FileText = typer.Argument(
        default="-", mode="r", help="file containing cve's in the jsonl format"
    ),
) -> None:
    """
    Filter specific CVE's from the input


    Input:
    { "cve": "<cve-id>", "cwe": "<cwe-id>", "description": "<multiline string>", "coordinates": "<string>", "references": ["<url>", "<url>", ...] }
    """

    def _github(infile):
        to_be_filtered = {cve for _, cve in gh_security_issues()}
        stderr("Filtering:")
        for issue in to_be_filtered:
            stderr(f"{issue}")
        filtered_issues = [
            issue for issue in _issues(infile) if issue.cve not in to_be_filtered
        ]
        for issue in _issues_as_json_str(filtered_issues):
            stdout(issue)
        raise typer.Exit(code=0)

    def _pass_through(infile):
        for line in infile:
            stdout(line)
        raise typer.Exit(code=0)

    actions = {Filter.GitHubIssues: _github, Filter.PassThrough: _pass_through}
    action = actions[type]
    action(input_file)


@CVE_CLI.command(name="create")
def create(
    input_file: typer.FileText = typer.Argument(
        default="-", mode="r", help="file of cve's in the jsonl format"
    ),
    project: str = typer.Option(
        default="", help="Project the created ticket shall be associated with."
    ),
) -> None:
    """
    Create GitHub issues for CVE's

    Input:
    { "cve": "<cve-id>", "cwe": "<cwe-id>", "description": "<multiline string>", "coordinates": "<string>", "references": ["<url>", "<url>", ...] }

    Output:
    Links to the created issue(s)
    """
    for issue in _issues(input_file):
        std_err, issue_url = create_security_issue(issue, project)
        stderr(std_err)
        stdout(format_jsonl(issue_url, issue))


class PPrintFormats(str, Enum):
    markdown = "markdown"


@CLI.command(name="pretty-print")
def json_issue_to_markdown(
    json_file: typer.FileText = typer.Argument(
        mode="r", help="json file with issues to convert"
    ),
    path: Path = typer.Argument(default=Path("."), help="path to project root"),
) -> None:
    content = json_file.read()
    issues = from_json(content, path.absolute())
    issues = sorted(issues, key=lambda i: (i.file_name, i.cwe, i.test_id))
    print(issues_to_markdown(issues))


def format_jsonl(issue_url: str, issue: Issue) -> str:
    issue_json = asdict(issue)
    issue_json["issue_url"] = issue_url.strip()
    return json.dumps(issue_json)


if __name__ == "__main__":
    CLI()
