from unittest.mock import patch

import pytest
from nox.sessions import _SessionQuit
from pydantic import computed_field

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._workflow import (
    audit_workflows,
    check_workflow,
    generate_workflow,
)
from exasol.toolbox.util.workflows.templates import (
    DOCUMENTATION_ONLY_WORKFLOW_NAMES,
    WORKFLOW_TEMPLATE_OPTIONS,
)
from exasol.toolbox.util.workflows.workflow_orchestrator import ALL


@pytest.fixture
def project_config_without_patcher(tmp_path) -> BaseConfig:
    class Config(BaseConfig):
        @computed_field  # type: ignore[misc]
        @property
        def github_workflow_patcher_yaml(self) -> None:
            """
            Override for testing purposes
            """
            return None

    return Config(
        root_path=tmp_path,
        project_name="test",
    )


@pytest.fixture
def project_config_without_documentation(tmp_path) -> BaseConfig:
    class Config(BaseConfig):
        @computed_field  # type: ignore[misc]
        @property
        def has_documentation(self) -> bool:
            return False

    return Config(
        root_path=tmp_path,
        project_name="test",
    )


@pytest.fixture
def nox_session_runner_posargs(request):
    value = request.param
    return list(value) if isinstance(value, (list, tuple)) else [value]


class TestGenerateWorkflow:
    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs, expected_count",
        [(ALL, 14), *[(key, 1) for key in WORKFLOW_TEMPLATE_OPTIONS.keys()]],
        indirect=["nox_session_runner_posargs"],
    )
    def test_works_as_expected(
        nox_session,
        project_config_without_patcher,
        nox_session_runner_posargs,
        expected_count,
    ):
        with patch(
            "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
            new=project_config_without_patcher,
        ):
            generate_workflow(nox_session)

        count = sum(
            1
            for _ in project_config_without_patcher.github_workflow_directory.glob(
                "*.yml"
            )
        )
        assert count == expected_count

    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        ["not-a-valid-name"],
        indirect=["nox_session_runner_posargs"],
    )
    def test_raises_exception_when_name_incorrect(
        nox_session, project_config_without_patcher, capsys, nox_session_runner_posargs
    ):
        with patch(
            "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
            new=project_config_without_patcher,
        ):

            with pytest.raises(SystemExit):
                generate_workflow(nox_session)

            assert "invalid choice: 'not-a-valid-name'" in capsys.readouterr().err

    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs, expected_count",
        [(ALL, 12)],
        indirect=["nox_session_runner_posargs"],
    )
    def test_skips_documentation_workflows_when_docs_disabled(
        nox_session,
        project_config_without_documentation,
        nox_session_runner_posargs,
        expected_count,
    ):
        with patch(
            "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
            new=project_config_without_documentation,
        ):
            generate_workflow(nox_session)

        count = sum(
            1
            for _ in project_config_without_documentation.github_workflow_directory.glob(
                "*.yml"
            )
        )
        assert count == expected_count
        existing_workflows = {
            workflow.name
            for workflow in project_config_without_documentation.github_workflow_directory.glob(
                "*.yml"
            )
        }
        assert {f"{name}.yml" for name in DOCUMENTATION_ONLY_WORKFLOW_NAMES}.isdisjoint(
            existing_workflows
        )


class TestCheckWorkflow:
    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        [ALL],
        indirect=["nox_session_runner_posargs"],
    )
    def test_passes_when_workflows_are_up_to_date_after_generation(
        nox_session,
        project_config_without_patcher,
        capsys,
        nox_session_runner_posargs,
    ):
        with patch(
            "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
            new=project_config_without_patcher,
        ):
            generate_workflow(nox_session)
            capsys.readouterr()

            check_workflow(nox_session)

        assert "--- existing:" not in capsys.readouterr().out

    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        [ALL],
        indirect=["nox_session_runner_posargs"],
    )
    def test_raises_session_quit_when_workflows_are_out_of_date(
        nox_session,
        project_config_without_patcher,
        nox_session_runner_posargs,
    ):
        with (
            patch("exasol.toolbox.util.workflows.workflow_orchestrator.logger.info"),
            patch(
                "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
                new=project_config_without_patcher,
            ),
        ):
            with pytest.raises(_SessionQuit) as exc:
                check_workflow(nox_session)

        assert str(exc.value) == (
            "\n13 workflows are out of date:\n"
            "- build-and-publish\n"
            "- cd\n"
            "- check-release-tag\n"
            "- checks\n"
            "- ci\n"
            "- dependency-update\n"
            "- fast-tests\n"
            "- gh-pages\n"
            "- matrix\n"
            "- merge-gate\n"
            "- periodic-validation\n"
            "- pr-merge\n"
            "- report"
        )

    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        [ALL],
        indirect=["nox_session_runner_posargs"],
    )
    def test_raises_session_quit_without_documentation_workflows(
        nox_session,
        project_config_without_documentation,
        nox_session_runner_posargs,
    ):
        with (
            patch("exasol.toolbox.util.workflows.workflow_orchestrator.logger.info"),
            patch(
                "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
                new=project_config_without_documentation,
            ),
        ):
            with pytest.raises(_SessionQuit) as exc:
                check_workflow(nox_session)

        assert str(exc.value) == (
            "\n11 workflows are out of date:\n"
            "- build-and-publish\n"
            "- cd\n"
            "- check-release-tag\n"
            "- checks\n"
            "- ci\n"
            "- dependency-update\n"
            "- fast-tests\n"
            "- matrix\n"
            "- merge-gate\n"
            "- periodic-validation\n"
            "- report"
        )


class TestAuditWorkflows:
    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        [["--version"]],
        indirect=["nox_session_runner_posargs"],
    )
    def test_passes_through_extra_arguments(
        nox_session,
        project_config_without_patcher,
        nox_session_runner_posargs,
    ):
        config_path = project_config_without_patcher.root_path / ".zizmor.yml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("rules: []\n")

        with (
            patch(
                "exasol.toolbox.nox._workflow.PROJECT_CONFIG",
                new=project_config_without_patcher,
            ),
            patch("nox.sessions.Session.run") as run_mock,
        ):
            audit_workflows(nox_session)

        run_mock.assert_called_once_with(
            "zizmor",
            "--config",
            config_path,
            "--version",
            project_config_without_patcher.root_path,
        )
