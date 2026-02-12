from inspect import cleandoc
from pathlib import Path

import pytest
from pydantic import ValidationError

from exasol.toolbox.util.workflows.patch_workflow import (
    ActionType,
    InvalidWorkflowPatcherYamlError,
    WorkflowPatcher,
)
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def workflow_patcher() -> WorkflowPatcher:
    return WorkflowPatcher(github_template_dict=PROJECT_CONFIG.github_template_dict)


@pytest.fixture
def workflow_patcher_yaml(tmp_path: Path) -> Path:
    return tmp_path / ".workflow-patcher.yml"


class TestWorkflowPatcher:
    @staticmethod
    def test_remove_jobs(example_patcher_yaml, workflow_patcher_yaml, workflow_patcher):
        content = cleandoc(example_patcher_yaml.remove_jobs)
        workflow_patcher_yaml.write_text(content)

        yaml_dict = workflow_patcher.get_yaml_dict(workflow_patcher_yaml)

        assert workflow_patcher.get_as_string(yaml_dict) == content

    @staticmethod
    @pytest.mark.parametrize("action", ActionType)
    def test_step_customizations(
        example_patcher_yaml, workflow_patcher_yaml, action, workflow_patcher
    ):
        content = cleandoc(
            example_patcher_yaml.step_customization.format(action=action.value)
        )
        workflow_patcher_yaml.write_text(content)

        yaml_dict = workflow_patcher.get_yaml_dict(workflow_patcher_yaml)

        assert workflow_patcher.get_as_string(yaml_dict) == content


class TestStepCustomization:
    @staticmethod
    def test_allows_extra_field(
        example_patcher_yaml, workflow_patcher_yaml, workflow_patcher
    ):
        content = f"""
        {example_patcher_yaml.step_customization.format(action="REPLACE")}
                  extra-field: "test"
        """
        content = cleandoc(content)
        workflow_patcher_yaml.write_text(content)

        yaml_dict = workflow_patcher.get_yaml_dict(workflow_patcher_yaml)

        assert workflow_patcher.get_as_string(yaml_dict) == content

    @staticmethod
    def test_raises_error_for_unknown_action(
        example_patcher_yaml, workflow_patcher_yaml, workflow_patcher
    ):
        content = cleandoc(
            example_patcher_yaml.step_customization.format(action="UNKNOWN")
        )
        workflow_patcher_yaml.write_text(content)

        with pytest.raises(
            InvalidWorkflowPatcherYamlError,
            match="is malformed; it failed Pydantic validation",
        ) as exc:
            workflow_patcher.get_yaml_dict(workflow_patcher_yaml)

        underlying_error = exc.value.__cause__
        assert isinstance(underlying_error, ValidationError)
