from unittest.mock import Mock

from exasol.toolbox.nox import _dependencies
from exasol.toolbox.util.dependencies.audit import Vulnerabilities


def test_audit(monkeypatch, nox_session, sample_vulnerability, capsys):
    monkeypatch.setattr(_dependencies, "Vulnerabilities", Mock())
    _dependencies.Vulnerabilities.load_from_pip_audit.return_value = Vulnerabilities(
        vulnerabilities=[sample_vulnerability.vulnerability]
    )
    _dependencies.audit(nox_session)
    assert capsys.readouterr().out == sample_vulnerability.nox_dependencies_audit


def test_report_resolved_vulnerabilities(monkeypatch, nox_session, capsys, sample_vulnerability):
    monkeypatch.setattr(
        _dependencies,
        "get_vulnerabilities_from_latest_tag",
        Mock(return_value=[sample_vulnerability.vulnerability]),
    )
    monkeypatch.setattr(_dependencies, "get_vulnerabilities", Mock(return_value=[]))
    _dependencies.report_resolved_vulnerabilities(nox_session)
    assert "| jinja2 | CVE-2025-27516 | 3.1.5 | 3.1.6 |" in capsys.readouterr().out
