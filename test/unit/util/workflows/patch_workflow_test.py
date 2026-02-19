from inspect import cleandoc
from pathlib import Path

import pytest
from pydantic import ValidationError
from ruamel.yaml import CommentedMap

from exasol.toolbox.util.workflows.exceptions import InvalidWorkflowPatcherYamlError
from exasol.toolbox.util.workflows.patch_workflow import (
    ActionType,
    WorkflowPatcher,
)
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def workflow_patcher_yaml(tmp_path: Path) -> Path:
    return tmp_path / ".workflow-patcher.yml"


@pytest.fixture
def workflow_patcher(workflow_patcher_yaml) -> WorkflowPatcher:
    return WorkflowPatcher(
        github_template_dict=PROJECT_CONFIG.github_template_dict,
        file_path=workflow_patcher_yaml,
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

    @staticmethod
    def test_extract_by_workflow_works_as_expected(
        example_patcher_yaml, workflow_patcher_yaml, workflow_patcher
    ):
        content = f"""
        {example_patcher_yaml.remove_jobs}
        - name: "pr-merge"
          remove_jobs:
           - publish-docs
        """
        content = cleandoc(content)
        workflow_patcher_yaml.write_text(content)

        result = workflow_patcher.extract_by_workflow("pr-merge")
        assert result == CommentedMap(
            {"name": "pr-merge", "remove_jobs": ["publish-docs"]}
        )

    @staticmethod
    def test_extract_by_workflow_not_found_returns_none(
        remove_job_yaml, workflow_patcher
    ):
        result = workflow_patcher.extract_by_workflow("pr-merge.yml")
        assert result is None


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
        ) as ex:
            workflow_patcher.content

        underlying_error = ex.value.__cause__
        assert isinstance(underlying_error, ValidationError)
        assert "Input should be 'INSERT_AFTER' or 'REPLACE'" in str(underlying_error)


class TestWorkflow:
    @staticmethod
    def test_raises_error_for_unknown_workflow_name(
        workflow_patcher_yaml, workflow_patcher
    ):
        content = """
        workflows:
        - name: "unknown-workflow"
          remove_jobs:
            - build-documentation-and-check-links
        """
        workflow_patcher_yaml.write_text(cleandoc(content))

        with pytest.raises(
            InvalidWorkflowPatcherYamlError,
            match="is malformed; it failed Pydantic validation",
        ) as ex:
            workflow_patcher.content

        underlying_error = ex.value.__cause__
        assert isinstance(underlying_error, ValidationError)
        assert "Invalid workflow: unknown-workflow. Must be one of dict_keys([" in str(
            underlying_error
        )
