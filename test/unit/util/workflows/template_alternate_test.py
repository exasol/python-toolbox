from inspect import cleandoc
from test.unit.util.workflows.template_test import (
    TEMPLATE,
    WORKFLOW,
)

from exasol.toolbox.util.workflows.template_alternate import TemplateToWorkflow
from noxconfig import PROJECT_CONFIG


class TestTemplateToWorkflow:
    @staticmethod
    def test_works_as_expected():
        template_to_workflow = TemplateToWorkflow(
            template_str=TEMPLATE,
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )
        assert template_to_workflow.convert() == cleandoc(WORKFLOW)
