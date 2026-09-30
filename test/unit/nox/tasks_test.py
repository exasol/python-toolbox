from unittest.mock import Mock, patch

from exasol.toolbox.nox import tasks


def test_check_runs_all_project_checks():
    session = Mock()
    context = {"coverage": True, "db_version": "8.29.13", "fwd-args": []}
    files = ("example.py",)

    with (
        patch.object(tasks, "_integration_test_context", return_value=context),
        patch.object(tasks, "get_filtered_python_files", return_value=files),
        patch.object(tasks, "_code_format") as code_format,
        patch.object(tasks, "_pylint") as pylint,
        patch.object(tasks, "_type_check") as type_check,
        patch.object(tasks, "_coverage") as coverage,
    ):
        tasks.check(session)

    code_format.assert_called_once_with(session, tasks.Mode.Check, files)
    pylint.assert_called_once_with(session, files)
    type_check.assert_called_once_with(session, files)
    coverage.assert_called_once_with(session, tasks.PROJECT_CONFIG, context)
