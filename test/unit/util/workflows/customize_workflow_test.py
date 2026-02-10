from dataclasses import dataclass
from inspect import cleandoc

import pytest
from pydantic import ValidationError

from exasol.toolbox.util.workflows.customize_workflow import (
    ActionType,
    WorkflowPatcher,
)
from noxconfig import PROJECT_CONFIG


@dataclass(frozen=True)
class ExampleYaml:
    remove_jobs = """
        workflows:
        - name: "checks.yml"
          remove_jobs:
            - documentation
        """
    step_customization = """
        workflows:
        - name: "checks.yml"
          step_customizations:
            - action: {action}
              job: Tests
              step_id: checkout-repo
              content:
                name: SCM Checkout
                id: checkout-repo
                uses: actions/checkout@v6
                with:
                  fetch-depth: 0
        """


@pytest.fixture
def workflow_patcher() -> WorkflowPatcher:
    return WorkflowPatcher(github_template_dict=PROJECT_CONFIG.github_template_dict)


class TestWorkflowPatcher:
    @staticmethod
    def test_remove_jobs(tmp_path, workflow_patcher):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = cleandoc(ExampleYaml.remove_jobs)
        file_path.write_text(content)

        yaml_dict = workflow_patcher.get_yaml_dict(file_path)

        assert workflow_patcher.get_as_string(yaml_dict) == content

    @staticmethod
    @pytest.mark.parametrize("action", ActionType)
    def test_step_customizations(tmp_path, action, workflow_patcher):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = cleandoc(ExampleYaml.step_customization.format(action=action.value))
        file_path.write_text(content)

        yaml_dict = workflow_patcher.get_yaml_dict(file_path)

        assert workflow_patcher.get_as_string(yaml_dict) == content


class TestStepCustomization:
    @staticmethod
    def test_allows_extra_field(tmp_path, workflow_patcher):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = f"""
        {ExampleYaml.step_customization.format(action="REPLACE")}
                  extra-field: "test"
        """
        content = cleandoc(content)
        file_path.write_text(content)

        yaml_dict = workflow_patcher.get_yaml_dict(file_path)

        assert workflow_patcher.get_as_string(yaml_dict) == content

    @staticmethod
    def test_raises_error_for_unknown_action(tmp_path, workflow_patcher):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = cleandoc(ExampleYaml.step_customization.format(action="UNKNOWN"))
        file_path.write_text(content)

        with pytest.raises(ValidationError, match="Input should be"):
            workflow_patcher.get_yaml_dict(file_path)
