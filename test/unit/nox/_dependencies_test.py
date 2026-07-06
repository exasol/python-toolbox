from pathlib import Path
from unittest.mock import Mock

import pytest

from exasol.toolbox.nox import _dependencies
from exasol.toolbox.util.dependencies.audit import Vulnerabilities


def test_audit(monkeypatch, nox_session, sample_vulnerability, capsys):
    monkeypatch.setattr(
        _dependencies.Vulnerabilities,
        "load_from_pip_audit",
        Mock(
            return_value=Vulnerabilities(
                vulnerabilities=[sample_vulnerability.vulnerability]
            )
        ),
    )
    _dependencies.audit(nox_session)
    assert capsys.readouterr().out == sample_vulnerability.nox_dependencies_audit


class TestUpdateVulnerabilities:
    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs", [["vulnerabilities.json"]], indirect=True
    )
    def test_writes_report_when_path_is_provided(
        monkeypatch, nox_session, tmp_path, nox_session_runner_posargs
    ):
        delegate = Mock(return_value="[]")
        monkeypatch.setattr(
            _dependencies.DependencyUpdater,
            "update_vulnerable_dependencies",
            delegate,
        )
        report_path = tmp_path / "vulnerabilities.json"

        _dependencies.update_vulnerabilities(nox_session)

        assert delegate.call_count == 1
        assert report_path.read_text() == "[]\n"

    @staticmethod
    def test_does_not_write_report_when_path_is_unset(
        monkeypatch, nox_session, tmp_path
    ):
        delegate = Mock(return_value="[]")
        monkeypatch.setattr(
            _dependencies.DependencyUpdater,
            "update_vulnerable_dependencies",
            delegate,
        )
        write_text = Mock()
        monkeypatch.setattr(Path, "write_text", write_text, raising=False)

        _dependencies.update_vulnerabilities(nox_session)

        assert delegate.call_count == 1
        write_text.assert_not_called()
