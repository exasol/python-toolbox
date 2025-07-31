import json
from inspect import cleandoc
from typing import Union

import pytest

from exasol.toolbox.tools.security import Issue
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


@pytest.fixture(scope="session")
def sample_vulnerability() -> SampleVulnerability:
    return SampleVulnerability()
