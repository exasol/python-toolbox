import json

from exasol.toolbox.nox._dependencies import Audit


class TestFilterJsonForVulnerabilities:

    @staticmethod
    def test_no_vulnerability_returns_empty_list():
        audit_dict = {
            "dependencies": [{"name": "alabaster", "version": "0.7.16", "vulns": []}]
        }
        audit_json = json.dumps(audit_dict).encode("utf-8")
        expected = {"dependencies": []}

        actual = Audit._filter_json_for_vulnerabilities(audit_json)
        assert actual == expected

    @staticmethod
    def test_vulnerabilities_returned_in_list(pip_audit_report):
        audit_json = json.dumps(pip_audit_report).encode("utf-8")

        actual = Audit._filter_json_for_vulnerabilities(audit_json)
        assert actual == pip_audit_report
