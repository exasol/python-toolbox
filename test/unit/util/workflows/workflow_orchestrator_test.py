import pytest

from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS
from exasol.toolbox.util.workflows.workflow_orchestrator import WorkflowOrchestrator


class TestTemplates:
    @staticmethod
    def test_all_works_as_expected():
        result = WorkflowOrchestrator(workflow_choice="all").templates
        assert result == WORKFLOW_TEMPLATE_OPTIONS

    @staticmethod
    @pytest.mark.parametrize("workflow_name", WORKFLOW_TEMPLATE_OPTIONS)
    def test_individual_workflows_works_as_expected(workflow_name):
        result = WorkflowOrchestrator(workflow_choice=workflow_name).templates
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
