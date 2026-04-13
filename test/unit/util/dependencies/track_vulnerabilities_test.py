from exasol.toolbox.util.dependencies.track_vulnerabilities import (
    DependenciesAudit,
    VulnerabilityMatcher,
)


class TestVulnerabilityMatcher:
    def test_not_resolved(self, sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        matcher = VulnerabilityMatcher(current_vulnerabilities=[vuln])
        assert not matcher.is_resolved(vuln)

    def test_changed_id_not_resolved(
        self, sample_vulnerability, flipped_id_vulnerability
    ):
        matcher = VulnerabilityMatcher(
            current_vulnerabilities=[flipped_id_vulnerability]
        )
        assert not matcher.is_resolved(sample_vulnerability.vulnerability)

    def test_resolved(self, sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        matcher = VulnerabilityMatcher(current_vulnerabilities=[])
        assert matcher.is_resolved(vuln)


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
