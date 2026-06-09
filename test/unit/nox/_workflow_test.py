from unittest.mock import patch

import pytest
from nox.sessions import _SessionQuit
from pydantic import computed_field

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._workflow import (
    check_workflow,
    generate_workflow,
)
from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS
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
def nox_session_runner_posargs(request):
    return [request.param]


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
            "\n14 workflows are out of date:\n"
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
            "- report\n"
            "- slow-checks"
        )
