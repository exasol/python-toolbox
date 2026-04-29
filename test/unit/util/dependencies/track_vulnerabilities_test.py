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


PKG_DATA = {"name": "cryptography", "version": "46.0.6"}

VULN_1 = Vulnerability(
    package=PKG_DATA,
    id="GHSA-m959-cc7f-wv43",
    aliases=["CVE-2026-34073"],
    fix_versions=["46.0.6"],
    description="Dummy description",
)

VULN_2 = Vulnerability(
    package=PKG_DATA,
    id="GHSA-p423-j2cm-9vmq",
    aliases=["CVE-2026-39892"],
    fix_versions=["46.0.7"],
    description="Dummy description",
)


class TestVulnerabilityMatcher:
    @staticmethod
    def test_not_resolved(sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        matcher = VulnerabilityMatcher(current_vulnerabilities=[vuln])
        assert not matcher.is_resolved(vuln)

    @staticmethod
    def test_changed_id_not_resolved(sample_vulnerability, flipped_id_vulnerability):
        """
        Simulate a vulnerability to be still present, but its ID having
        changed over time.

        The test verifies that the vulnerability (using the original ID) is
        still matched as "not resolved".
        """

        matcher = VulnerabilityMatcher(
            current_vulnerabilities=[flipped_id_vulnerability]
        )
        assert not matcher.is_resolved(sample_vulnerability.vulnerability)

    @staticmethod
    def test_resolved(sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        matcher = VulnerabilityMatcher(current_vulnerabilities=[])
        assert matcher.is_resolved(vuln)

    @staticmethod
    @pytest.mark.parametrize(
        "current_vulnerabilities",
        [
            [VULN_1, VULN_2],
            [VULN_2],
        ],
    )
    def test_no_resolution_same_package(current_vulnerabilities):
        """
        Two vulnerabilities in the same package 'cryptography', none of
        them resolved.
        """

        matcher = VulnerabilityMatcher(current_vulnerabilities=current_vulnerabilities)
        for v in (VULN_1, VULN_2):
            expected = not v in current_vulnerabilities
            assert matcher.is_resolved(v) is expected


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

    def test_resolved_vulnerability(self, sample_vulnerability):
        audit = DependenciesAudit(
            previous_vulnerabilities=[sample_vulnerability.vulnerability],
            current_vulnerabilities=[],
        )
        assert audit.resolved_vulnerabilities == [sample_vulnerability.vulnerability]
