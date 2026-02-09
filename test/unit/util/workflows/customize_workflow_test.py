import io
from dataclasses import dataclass
from inspect import cleandoc

import pytest
from pydantic import ValidationError

from exasol.toolbox.util.workflows.customize_workflow import (
    ActionType,
    load_and_validate_workflow_customizer,
)
from exasol.toolbox.util.workflows.format_yaml import get_standard_yaml


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
                  # The PTB has unit tests which require the fetch-depth to be 0.
                  with:
                    fetch-depth: 0
        """


def convert_back_to_str(yaml_dict):
    stream = io.StringIO()
    yaml = get_standard_yaml()
    yaml.dump(yaml_dict, stream)
    return stream.getvalue()


class TestLoadAndValidateWorkflowCustomizer:
    @staticmethod
    def test_remove_jobs(tmp_path):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = cleandoc(ExampleYaml.remove_jobs)
        file_path.write_text(content)

        result = load_and_validate_workflow_customizer(file_path)

        assert convert_back_to_str(result) == content + "\n"

    @staticmethod
    @pytest.mark.parametrize("action", ActionType)
    def test_step_customizations(tmp_path, action):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = cleandoc(ExampleYaml.step_customization.format(action=action.value))
        file_path.write_text(content)

        result = load_and_validate_workflow_customizer(file_path)

        assert convert_back_to_str(result) == content + "\n"


class TestStepCustomization:
    @staticmethod
    def test_allows_extra_field(tmp_path):
        file_path = tmp_path / ".exasol-toolbox.yml"

        content = f"""
        {ExampleYaml.step_customization.format(action="REPLACE")}
                  extra-field: "test"
        """
        content = cleandoc(content)
        file_path.write_text(content)

        result = load_and_validate_workflow_customizer(file_path)

        assert convert_back_to_str(result) == content + "\n"

    @staticmethod
    def test_raises_error_for_unknown_action(tmp_path):
        file_path = tmp_path / ".exasol-toolbox.yml"
        content = cleandoc(ExampleYaml.step_customization.format(action="UNKNOWN"))
        file_path.write_text(content)

        with pytest.raises(ValidationError, match="Input should be"):
            load_and_validate_workflow_customizer(file_path)
