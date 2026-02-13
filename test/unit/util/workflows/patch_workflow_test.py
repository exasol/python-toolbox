from inspect import cleandoc

import pytest
from pydantic import ValidationError

from exasol.toolbox.util.workflows.patch_workflow import (
    ActionType,
    InvalidWorkflowPatcherYamlError,
)


class TestWorkflowPatcher:
    @staticmethod
    def test_remove_jobs(remove_job_yaml, workflow_patcher):
        result = workflow_patcher.content
        assert workflow_patcher.get_as_string(result) == remove_job_yaml

    @staticmethod
    @pytest.mark.parametrize(
        "step_customization_yaml",
        [action.value for action in ActionType],
        indirect=True,
    )
    def test_step_customizations(step_customization_yaml, workflow_patcher):
        result = workflow_patcher.content
        assert workflow_patcher.get_as_string(result) == step_customization_yaml


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

        yaml_dict = workflow_patcher.get_yaml_dict()

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
            workflow_patcher.content

        underlying_error = exc.value.__cause__
        assert isinstance(underlying_error, ValidationError)
