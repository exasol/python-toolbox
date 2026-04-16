import pytest

from exasol.toolbox.util.dependencies.audit import Vulnerability
from exasol.toolbox.util.dependencies.track_vulnerabilities import (
    DependenciesAudit,
    VulnerabilityMatcher,
)


@pytest.fixture
def flipped_id_vulnerability(sample_vulnerability) -> Vulnerability:
    """
    Returns an instance of SampleVulnerability equal to
    sample_vulnerability() but with ID and first alias flipped to verify
    handling of vulnerabilities with changed ID.
    """

    other = sample_vulnerability
    vuln_entry = {
        "aliases": [other.cve_id],
        "id": other.vulnerability_id,
        "fix_versions": other.vulnerability.fix_versions,
        "description": other.description,
    }
    return Vulnerability.from_audit_entry(
        package_name=other.package_name,
        version=other.version,
        vuln_entry=vuln_entry,
    )


class TestVulnerabilityMatcher:
    def test_not_resolved(self, sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        matcher = VulnerabilityMatcher(current_vulnerabilities=[vuln])
        assert not matcher.is_resolved(vuln)

    def test_changed_id_not_resolved(
        self, sample_vulnerability, flipped_id_vulnerability
    ):
        """
        Simulate a vulnerability to be still present, but it's ID having
        changed over time.

        The test verifies that the vulnerability (using the original ID) is
        still matched as "not resolved".
        """

        matcher = VulnerabilityMatcher(
            current_vulnerabilities=[flipped_id_vulnerability]
        )
        assert not matcher.is_resolved(sample_vulnerability.vulnerability)

    def test_resolved(self, sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        matcher = VulnerabilityMatcher(current_vulnerabilities=[])
        assert matcher.is_resolved(vuln)

    def test_no_resolution_same_package(self):
        """
        Scenario: 'cryptography' has two vulnerabilities.
        One is resolved (removed from the current list), the other remains.
        """
        pkg_data = {"name": "cryptography", "version": "46.0.6"}

        vuln_1 = Vulnerability(
            package=pkg_data,
            id="GHSA-m959-cc7f-wv43",
            aliases=["CVE-2026-34073"],
            fix_versions=["46.0.6"],
            description="Dummy description",
        )

        vuln_2 = Vulnerability(
            package=pkg_data,
            id="GHSA-p423-j2cm-9vmq",
            aliases=["CVE-2026-39892"],
            fix_versions=["46.0.7"],
            description="Dummy description",
        )

        matcher = VulnerabilityMatcher(current_vulnerabilities=[vuln_1, vuln_2])

        assert matcher.is_resolved(vuln_1) is False
        assert matcher.is_resolved(vuln_2) is False


class TestDependenciesAudit:
    def test_no_vulnerabilities_for_previous_and_current(self):
        audit = DependenciesAudit(
            previous_vulnerabilities=[], current_vulnerabilities=[]
        )
        assert audit.resolved_vulnerabilities == []

    def test_vulnerability_in_current_but_not_present(self, sample_vulnerability):
        audit = DependenciesAudit(
            previous_vulnerabilities=[],
            current_vulnerabilities=[sample_vulnerability.vulnerability],
        )
        # only care about "resolved" vulnerabilities, not new ones
        assert audit.resolved_vulnerabilities == []

    def test_resolved_vulnerabilities(self, sample_vulnerability):
        audit = DependenciesAudit(
            previous_vulnerabilities=[sample_vulnerability.vulnerability],
            current_vulnerabilities=[],
        )
        assert audit.resolved_vulnerabilities == [sample_vulnerability.vulnerability]
