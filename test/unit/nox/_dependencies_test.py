from unittest.mock import Mock

import pytest

from exasol.toolbox.nox import _dependencies
from exasol.toolbox.nox import _shared as nox_shared
from exasol.toolbox.util.dependencies.audit import Vulnerabilities


@pytest.mark.parametrize(
    ("was_updated", "report_json", "expected"),
    [
        (False, "[]", "No vulnerable dependencies were found."),
        (True, "[]", "No vulnerable dependencies remain after updating."),
        (True, '{"a": 1}', '{"a": 1}'),
    ],
)
def test_format_update_vulnerabilities_message(was_updated, report_json, expected):
    assert (
        _dependencies._format_update_vulnerabilities_message(was_updated, report_json)
        == expected
    )


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
    def test_writes_report_when_path_is_provided(
        monkeypatch, nox_session, tmp_path, test_project_config_factory
    ):
        delegate = Mock(return_value=(True, "[]"))
        project_config = test_project_config_factory()
        monkeypatch.setattr(
            _dependencies.DependencyUpdater,
            "update_vulnerable_dependencies",
            delegate,
        )
        report_filename = "vulnerabilities.json"
        report_path = tmp_path / report_filename
        nox_session._runner.posargs = [report_filename]

        monkeypatch.setattr(_dependencies, "PROJECT_CONFIG", project_config)
        monkeypatch.setattr(nox_shared, "PROJECT_CONFIG", project_config)
        _dependencies.update_vulnerabilities(nox_session)

        assert delegate.call_count == 1
        assert report_path.read_text() == "[]\n"

    @staticmethod
    def test_does_not_write_report_when_path_is_unset(monkeypatch, nox_session, capsys):
        delegate = Mock(return_value=(False, "[]"))
        monkeypatch.setattr(
            _dependencies.DependencyUpdater,
            "update_vulnerable_dependencies",
            delegate,
        )

        _dependencies.update_vulnerabilities(nox_session)

        assert delegate.call_count == 1
        assert capsys.readouterr().out == "No vulnerable dependencies were found.\n"
