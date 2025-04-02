from __future__ import annotations

import json
from collections.abc import Generator
from dataclasses import (
    asdict,
    dataclass,
)
from enum import Enum
from typing import Iterable

import typer


@dataclass(frozen=True)
class VulnerabilityIssue:
    """
    Dataclass for a vulnerability to be submitted to GitHub as an issue.

    This format does not reflect the official CVE JSON schema:
    https://github.com/CVEProject/cve-schema/blob/master/schema/v5.0/CVE_JSON_5.0_schema.json
    Additionally, it is a known that some vulnerabilities may not initially or ever be
    assigned a CVE, which is meant to act as a unique identifier. In such cases, they
    instead have another kind of vulnerability ID associated with them.
    """

    cve: str
    cwe: str
    description: str
    coordinates: str
    references: tuple

    @staticmethod
    def extract_from_jsonl(jsonl: typer.FileText) -> Generator[VulnerabilityIssue]:
        """Converts the lines of a JSONL file into a generator of VulnerabilityIssue"""
        lines = (l for l in jsonl if l.strip() != "")
        for line in lines:
            obj = json.loads(line)
            obj["references"] = tuple(obj["references"])
            yield VulnerabilityIssue(**obj)

    @property
    def json_str(self) -> str:
        """Converts to a string-encoded JSON"""
        issue = asdict(self)
        return json.dumps(issue)


@dataclass(frozen=True)
class GitHubVulnerabilityIssue:
    """Dataclass for an existing GitHub Issue associated with a vulnerability."""

    cve: str
    cwe: str
    description: str
    coordinates: str
    references: tuple
    issue_url: str

    @staticmethod
    def from_vulnerability_issue(
        issue: VulnerabilityIssue, issue_url: str
    ) -> GitHubVulnerabilityIssue:
        """Converts VulnerabilityIssue to GitHubVulnerabilityIssue"""
        return GitHubVulnerabilityIssue(**asdict(issue), issue_url=issue_url.strip())

    @staticmethod
    def extract_from_jsonl(
        jsonl: typer.FileText,
    ) -> Generator[GitHubVulnerabilityIssue]:
        """Converts the lines of a JSONL file into a generator of GitHubVulnerabilityIssue"""
        lines = (l for l in jsonl if l.strip() != "")
        for line in lines:
            obj = json.loads(line)
            obj["references"] = tuple(obj["references"])
            yield GitHubVulnerabilityIssue(**obj)

    @property
    def json_str(self) -> str:
        """Converts to a string-encoded JSON"""
        issue_json = asdict(self)
        return json.dumps(issue_json)


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


def from_pip_audit(report: str) -> Iterable[VulnerabilityIssue]:
    """
    Transforms the JSON output from `nox -s dependency:audit` into an iterable of
    `VulnerabilityIssue` objects.

    This does not gracefully handle scenarios where:
     - a CVE is not initially associated with the vulnerability; however, the assumption
     is that such vulnerabilities will later be associated with a CVE.
     - the same vulnerability ID (CVE, PYSEC, GHSA, etc.) is present across
     multiple coordinates.

    Input:
        '{"dependencies": [{"name": "<package_name>", "version": "<package_version>",
        "vulns": [{"id": "<vuln_id>", "fix_versions": ["<fix_version>"],
        "aliases": ["<vuln_id2>"], "description": "<vuln_description>"}]}]}'

    Args:
        report:
            the JSON output of `nox -s dependency:audit` provided as a str
    """
    report_dict = json.loads(report)
    dependencies = report_dict.get("dependencies", [])
    for dependency in dependencies:
        package = dependency["name"]
        for v in dependency["vulns"]:
            refs = [v["id"]] + v["aliases"]
            cves, cwes, links = identify_pypi_references(
                references=refs, package_name=package
            )
            if cves:
                yield VulnerabilityIssue(
                    cve=sorted(cves)[0],
                    cwe="None" if not cwes else ", ".join(cwes),
                    description=v["description"],
                    coordinates=f"{package}:{dependency['version']}",
                    references=tuple(links),
                )


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
