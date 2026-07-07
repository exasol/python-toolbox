from unittest import mock

import pytest

from exasol.toolbox.util.dependencies import update_dependencies
from exasol.toolbox.util.dependencies.audit import Vulnerabilities


@pytest.fixture
def mock_load_from_pip_audit(monkeypatch):
    load_from_pip_audit = mock.Mock()
    monkeypatch.setattr(
        update_dependencies.Vulnerabilities,
        "load_from_pip_audit",
        load_from_pip_audit,
    )
    return load_from_pip_audit


@pytest.fixture
def mock_subprocess_run(monkeypatch):
    run = mock.Mock()
    monkeypatch.setattr(update_dependencies.subprocess, "run", run)
    return run


def set_git_commands(monkeypatch, has_uncommitted_path_changes: bool):
    monkeypatch.setattr(
        update_dependencies.Git,
        "has_uncommitted_path_changes",
        mock.Mock(return_value=has_uncommitted_path_changes),
    )
    monkeypatch.setattr(update_dependencies.Git, "add", mock.Mock())
    monkeypatch.setattr(update_dependencies.Git, "commit", mock.Mock())


class TestUpdateVulnerableDependencies:
    @staticmethod
    def test_when_no_vulnerabilities_exits_early(
        monkeypatch, mock_load_from_pip_audit, mock_subprocess_run, tmp_path, capsys
    ):
        mock_load_from_pip_audit.side_effect = [Vulnerabilities(vulnerabilities=[])]

        updater = update_dependencies.DependencyUpdater(root_path=tmp_path)
        result = updater.update_vulnerable_dependencies()

        assert capsys.readouterr().out == ""
        mock_subprocess_run.assert_not_called()
        assert result == (False, "[]")

    @staticmethod
    def test_when_poetry_lock_is_not_updated(
        monkeypatch,
        mock_load_from_pip_audit,
        mock_subprocess_run,
        sample_vulnerability,
        tmp_path,
    ):
        mock_load_from_pip_audit.side_effect = [
            # Simulating the `poetry update` does not resolve the situation
            Vulnerabilities(vulnerabilities=[sample_vulnerability.vulnerability]),
        ] * 2
        set_git_commands(monkeypatch, has_uncommitted_path_changes=False)
        mock_subprocess_run.return_value = mock.Mock(returncode=0)

        updater = update_dependencies.DependencyUpdater(root_path=tmp_path)
        result = updater.update_vulnerable_dependencies()

        mock_subprocess_run.assert_called_once_with(
            ["poetry", "update"], cwd=tmp_path, check=True
        )
        update_dependencies.Git.add.assert_not_called()
        update_dependencies.Git.commit.assert_not_called()
        assert result == (True, sample_vulnerability.report_json)

    @staticmethod
    def test_when_poetry_lock_is_updated(
        monkeypatch,
        mock_load_from_pip_audit,
        mock_subprocess_run,
        sample_vulnerability,
        tmp_path,
    ):
        mock_load_from_pip_audit.side_effect = [
            # Simulating the `poetry update` resolves the vulnerabilities
            Vulnerabilities(vulnerabilities=[sample_vulnerability.vulnerability]),
            Vulnerabilities(vulnerabilities=[]),
        ]
        set_git_commands(monkeypatch, has_uncommitted_path_changes=True)
        mock_subprocess_run.return_value = mock.Mock(returncode=0)

        updater = update_dependencies.DependencyUpdater(root_path=tmp_path)
        result = updater.update_vulnerable_dependencies()

        assert mock_subprocess_run.call_args_list == [
            mock.call(["poetry", "update"], cwd=tmp_path, check=True),
        ]
        update_dependencies.Git.add.assert_called_once_with((updater.poetry_lock_path,))
        update_dependencies.Git.commit.assert_called_once_with("Updated poetry.lock")
        assert result == (True, "[]")
