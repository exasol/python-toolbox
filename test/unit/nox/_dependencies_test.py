from unittest import mock

from exasol.toolbox.nox._dependencies import audit
from exasol.toolbox.util.dependencies.audit import Vulnerabilities


class TestAudit:
    @staticmethod
    def test_works_as_expected_with_mock(nox_session, sample_vulnerability, capsys):
        with mock.patch(
            "exasol.toolbox.nox._dependencies.Vulnerabilities"
        ) as mock_class:
            mock_class.load_from_pip_audit.return_value = Vulnerabilities(
                vulnerabilities=[sample_vulnerability.vulnerability]
            )
            audit(nox_session)

        assert capsys.readouterr().out == sample_vulnerability.nox_dependencies_audit
