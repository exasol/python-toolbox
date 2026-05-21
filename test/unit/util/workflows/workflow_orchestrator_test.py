import pytest

from exasol.toolbox.util.workflows.templates import (
    NOT_MAINTAINED_WORKFLOW_NAMES,
    WORKFLOW_TEMPLATE_OPTIONS,
)
from exasol.toolbox.util.workflows.workflow_orchestrator import WorkflowOrchestrator


class TestTemplates:
    @staticmethod
    def test_all_works_as_expected(project_config):
        result = WorkflowOrchestrator(
            workflow_choice="all", config=project_config
        ).templates
        assert result == WORKFLOW_TEMPLATE_OPTIONS

    @staticmethod
    @pytest.mark.parametrize("workflow_name", WORKFLOW_TEMPLATE_OPTIONS)
    def test_individual_workflows_works_as_expected(workflow_name, project_config):
        result = WorkflowOrchestrator(
            workflow_choice=workflow_name, config=project_config
        ).templates
        assert result == {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}


class TestIsNewProject:
    @staticmethod
    def test_returns_true_when_no_yml_files_exist(project_config):
        project_config.github_workflow_directory.mkdir(parents=True)

        result = WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config,
        ).is_new_project

        assert result is True

    @staticmethod
    def test_returns_false_when_yml_files_exist(project_config):
        workflow_directory = project_config.github_workflow_directory
        workflow_directory.mkdir(parents=True)
        (workflow_directory / "existing.yml").touch()

        result = WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config,
        ).is_new_project

        assert result is False


class TestSkipWorkflow:
    @staticmethod
    def test_returns_true_for_not_maintained_workflow_in_existing_project(
        project_config,
    ):
        workflow_directory = project_config.github_workflow_directory
        workflow_directory.mkdir(parents=True)
        (workflow_directory / "existing.yml").touch()

        result = WorkflowOrchestrator(
            workflow_choice=NOT_MAINTAINED_WORKFLOW_NAMES[0],
            config=project_config,
        )._skip_workflow(
            workflow_name=NOT_MAINTAINED_WORKFLOW_NAMES[0],
            is_new_project=False,
        )

        assert result is True

    @staticmethod
    def test_returns_false_for_maintained_workflow(project_config):
        result = WorkflowOrchestrator(
            workflow_choice="checks",
            config=project_config,
        )._skip_workflow(workflow_name="checks", is_new_project=False)

        assert result is False
