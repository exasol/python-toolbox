from unittest.mock import Mock

from exasol.toolbox.nox import tasks
from exasol.toolbox.nox._shared import Mode


def test_project_check_runs_all_project_checks(monkeypatch, nox_session, tmp_path):
    config = Mock(root_path=tmp_path)
    context = {"coverage": True, "fwd-args": []}
    python_files = ["src/example.py"]
    integration_context = Mock(return_value=context)
    get_python_files = Mock(return_value=python_files)
    code_format = Mock()
    pylint = Mock()
    type_check = Mock()
    coverage = Mock()

    monkeypatch.setattr(tasks, "PROJECT_CONFIG", config)
    monkeypatch.setattr(tasks, "_integration_test_context", integration_context)
    monkeypatch.setattr(tasks, "get_filtered_python_files", get_python_files)
    monkeypatch.setattr(tasks, "_code_format", code_format)
    monkeypatch.setattr(tasks, "_pylint", pylint)
    monkeypatch.setattr(tasks, "_type_check", type_check)
    monkeypatch.setattr(tasks, "_coverage", coverage)

    tasks.check(nox_session)

    integration_context.assert_called_once_with(nox_session, coverage=True)
    get_python_files.assert_called_once_with(tmp_path)
    code_format.assert_called_once_with(nox_session, Mode.Check, python_files)
    pylint.assert_called_once_with(nox_session, python_files)
    type_check.assert_called_once_with(nox_session, python_files)
    coverage.assert_called_once_with(nox_session, config, context)
