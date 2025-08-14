import json
from inspect import cleandoc
from typing import Union

import pytest

from exasol.toolbox.tools import security
from exasol.toolbox.tools.security import (
    Issue,
    _issues_as_json_str,
)
from exasol.toolbox.util.dependencies.audit import Vulnerability


class SampleVulnerability:
    package_name = "jinja2"
    version = "3.1.5"
    fix_version = "3.1.6"
    vulnerability_id = "GHSA-cpwx-vrp4-4pq7"
    cve_id = "CVE-2025-27516"
    description = cleandoc(
        """An oversight in how the Jinja sandboxed environment interacts with the
        `|attr` filter allows an attacker that controls the content of a template
        to execute arbitrary Python code."""
    )

    @property
    def pip_audit_vuln_entry(self) -> dict[str, Union[str, list[str]]]:
        return {
            "id": self.vulnerability_id,
            "fix_versions": [self.fix_version],
            "aliases": [self.cve_id],
            "description": self.description,
        }

    @property
    def pip_audit_json(self) -> str:
        return json.dumps(
            {
                "dependencies": [
                    {
                        "name": self.package_name,
                        "version": self.version,
                        "vulns": [self.pip_audit_vuln_entry],
                    }
                ]
            }
        )

    @property
    def vulnerability(self) -> Vulnerability:
        return Vulnerability.from_audit_entry(
            package_name=self.package_name,
            version=self.version,
            vuln_entry=self.pip_audit_vuln_entry,
        )

    @property
    def nox_dependencies_audit(self) -> str:
        return json.dumps([self.security_issue_entry], indent=2) + "\n"

    @property
    def security_issue_entry(self) -> dict[str, Union[str, list[str]]]:
        return {
            "name": self.package_name,
            "version": self.version,
            "refs": [self.vulnerability_id, self.cve_id],
            "description": self.description,
        }

    @property
    def security_issue(self) -> Issue:
        return Issue(
            cve=self.cve_id,
            cwe="None",
            description=self.description,
            coordinates=f"{self.package_name}:{self.version}",
            references=(
                f"https://github.com/advisories/{self.vulnerability_id}",
                f"https://nvd.nist.gov/vuln/detail/{self.cve_id}",
            ),
        )


class SampleMavenVulnerabilities:
    gturri_issue = security.Issue(
        cve="CVE-2020-36641",
        cwe="CWE-611",
        description="A vulnerability classified as problematic was found in "
        "gturri aXMLRPC up to 1.12.0. This vulnerability affects "
        "the function ResponseParser of the file "
        "src/main/java/de/timroes/axmlrpc/ResponseParser.java. The "
        "manipulation leads to xml external entity reference. "
        "Upgrading to version 1.12.1 is able to address this issue. "
        "The patch is identified as "
        "ad6615b3ec41353e614f6ea5fdd5b046442a832b. It is "
        "recommended to upgrade the affected component. VDB-217450 "
        "is the identifier assigned to this vulnerability.\n"
        "\n"
        "Sonatype's research suggests that this CVE's details "
        "differ from those defined at NVD. See "
        "https://ossindex.sonatype.org/vulnerability/CVE-2020-36641 "
        "for details",
        coordinates="fr.turri:aXMLRPC:jar:1.13.0:test",
        references=(
            "https://ossindex.sonatype.org/vulnerability/CVE-2020-36641?component-type=maven&component-name=fr.turri%2FaXMLRPC&utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
            "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2020-36641",
            "https://www.tenable.com/cve/CVE-2020-36641",
        ),
    )
    github_issue_url = "https://github.com/exasol/a-project/issues/123"

    @property
    def report_json(self) -> str:
        return json.dumps(
            {
                "vulnerable": {
                    "fr.turri:aXMLRPC:jar:1.13.0:test": {
                        "coordinates": "pkg:maven/fr.turri/aXMLRPC@1.13.0",
                        "description": "Lightweight Java XML-RPC working also on Android.",
                        "reference": "https://ossindex.sonatype.org/component/pkg:maven/fr.turri/aXMLRPC@1.13.0?utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                        "vulnerabilities": [
                            {
                                "id": self.gturri_issue.cve,
                                "displayName": self.gturri_issue.cve,
                                "title": f"[{self.gturri_issue.cve}] {self.gturri_issue.cwe}: Improper Restriction of XML External Entity Reference ('XXE')",
                                "description": self.gturri_issue.description,
                                "cvssScore": 9.8,
                                "cvssVector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                                "cwe": self.gturri_issue.cwe,
                                "cve": self.gturri_issue.cve,
                                "reference": self.gturri_issue.references[0],
                                "externalReferences": self.gturri_issue.references[1:],
                            }
                        ],
                    },
                },
            }
        )

    @property
    def issues(self) -> set[Issue]:
        return {self.gturri_issue}

    @property
    def issues_json(self) -> str:
        convert_to_json = list(_issues_as_json_str(self.issues))
        return convert_to_json[0]

    @property
    def gh_security_issues(self):
        yield "I_kwDOKj3wMM50puMN", self.gturri_issue.cve

    @property
    def create_issues_json(self) -> str:
        issues_dict = json.loads(self.issues_json)
        issues_dict["issue_url"] = self.github_issue_url
        return json.dumps(issues_dict)


@pytest.fixture(scope="session")
def sample_vulnerability() -> SampleVulnerability:
    return SampleVulnerability()


@pytest.fixture(scope="session")
def sample_maven_vulnerabilities() -> SampleMavenVulnerabilities:
    return SampleMavenVulnerabilities()
