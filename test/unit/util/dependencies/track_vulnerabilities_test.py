from exasol.toolbox.util.dependencies.track_vulnerabilities import (
    ResolvedVulnerabilities,
)


class TestResolvedVulnerabilities:
    def test_vulnerability_present_for_previous_and_current(self, sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        resolved = ResolvedVulnerabilities(
            previous_vulnerabilities=[vuln], current_vulnerabilities=[vuln]
        )
        assert resolved._is_resolved(vuln) is False

    def test_vulnerability_present_for_previous_and_current_with_different_id(
        self, sample_vulnerability
    ):
        vuln2 = sample_vulnerability.vulnerability.__dict__.copy()
        vuln2["version"] = sample_vulnerability.version
        # flipping aliases & id to ensure can match across types
        vuln2["aliases"] = [sample_vulnerability.vulnerability_id]
        vuln2["id"] = sample_vulnerability.cve_id

        resolved = ResolvedVulnerabilities(
            previous_vulnerabilities=[sample_vulnerability.vulnerability],
            current_vulnerabilities=[vuln2],
        )
        assert resolved._is_resolved(sample_vulnerability.vulnerability) is False

    def test_vulnerability_in_previous_resolved_in_current(self, sample_vulnerability):
        vuln = sample_vulnerability.vulnerability
        resolved = ResolvedVulnerabilities(
            previous_vulnerabilities=[vuln], current_vulnerabilities=[]
        )
        assert resolved._is_resolved(vuln) is True

    def test_no_vulnerabilities_for_previous_and_current(self):
        resolved = ResolvedVulnerabilities(
            previous_vulnerabilities=[], current_vulnerabilities=[]
        )
        assert resolved.resolutions == []

    def test_vulnerability_in_current_but_not_present(self, sample_vulnerability):
        resolved = ResolvedVulnerabilities(
            previous_vulnerabilities=[],
            current_vulnerabilities=[sample_vulnerability.vulnerability],
        )
        # only care about "resolved" vulnerabilities, not new ones
        assert resolved.resolutions == []

    def test_resolved_vulnerabilities(self, sample_vulnerability):
        resolved = ResolvedVulnerabilities(
            previous_vulnerabilities=[sample_vulnerability.vulnerability],
            current_vulnerabilities=[],
        )
        assert resolved.resolutions == [sample_vulnerability.vulnerability]
