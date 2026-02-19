from unittest.mock import patch

import pytest
from pydantic import computed_field
from toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._workflow import update_workflow
from exasol.toolbox.util.workflows.workflow import ALL


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
    return ["--name", request.param]


class TestUpdateWorkflow:
    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs, expected_count",
        [(ALL, 13), *[(key, 1) for key in WORKFLOW_TEMPLATE_OPTIONS.keys()]],
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
            update_workflow(nox_session)

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
                update_workflow(nox_session)

            assert "invalid choice: 'not-a-valid-name'" in capsys.readouterr().err
