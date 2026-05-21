import pytest

from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS
from exasol.toolbox.util.workflows.workflow_orchestrator import WorkflowOrchestrator


class TestTemplates:
    @staticmethod
    def test_for_all_works_as_expected():
        result = WorkflowOrchestrator(workflow_choice="all").templates
        assert result == WORKFLOW_TEMPLATE_OPTIONS

    @staticmethod
    @pytest.mark.parametrize("workflow_name", WORKFLOW_TEMPLATE_OPTIONS)
    def test_for_individual_workflows_works_as_expected(workflow_name):
        result = WorkflowOrchestrator(workflow_choice=workflow_name).templates
        assert result == {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}
