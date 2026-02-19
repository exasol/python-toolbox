from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path

import pytest
from pydantic import (
    computed_field,
)

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.util.workflows.patch_workflow import WorkflowPatcher


@dataclass(frozen=True)
class ExamplePatcherYaml:
    remove_jobs = """
        workflows:
        - name: "checks"
          remove_jobs:
            - build-documentation-and-check-links
        """
    step_customization = """
        workflows:
        - name: "checks"
          step_customizations:
            - action: {action}
              job: run-unit-tests
              step_id: check-out-repository
              content:
                - name: Check out Repository
                  id: check-out-repository
                  uses: actions/checkout@v6
                  with:
                    fetch-depth: 0
        """


@pytest.fixture(scope="session")
def example_patcher_yaml():
    return ExamplePatcherYaml


@pytest.fixture
def workflow_patcher(project_config) -> WorkflowPatcher:
    return WorkflowPatcher(
        github_template_dict=project_config.github_template_dict,
        file_path=project_config.github_workflow_patcher_yaml,
    )


@pytest.fixture
def remove_job_yaml(example_patcher_yaml, project_config):
    content = cleandoc(example_patcher_yaml.remove_jobs)
    project_config.github_workflow_patcher_yaml.write_text(content)
    return content


@pytest.fixture
def step_customization_yaml(request, example_patcher_yaml, project_config):
    # request.param will hold the value passed from @pytest.mark.parametrize
    action_value = request.param

    text = example_patcher_yaml.step_customization.format(action=action_value)
    content = cleandoc(text)
    project_config.github_workflow_patcher_yaml.write_text(content)
    return content


@pytest.fixture
def project_config(tmp_path) -> BaseConfig:
    class Config(BaseConfig):
        @computed_field  # type: ignore[misc]
        @property
        def github_workflow_patcher_yaml(self) -> Path:
            """
            Override for testing purposes
            """
            return self.root_path / ".workflow-patcher.yml"

    return Config(
        root_path=tmp_path,
        project_name="test",
    )


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
