from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path

import pytest

from exasol.toolbox.util.workflows.patch_workflow import WorkflowPatcher
from noxconfig import PROJECT_CONFIG


@dataclass(frozen=True)
class ExamplePatcherYaml:
    remove_jobs = """
        workflows:
        - name: "checks.yml"
          remove_jobs:
            - build-documentation-and-check-links
        """
    step_customization = """
        workflows:
        - name: "checks.yml"
          step_customizations:
            - action: {action}
              job: run-unit-tests
              step_id: check-out-repository
              content:
                - name: SCM Checkout
                  id: checkout-repo
                  uses: actions/checkout@v6
                  with:
                    fetch-depth: 0
        """


@pytest.fixture(scope="session")
def example_patcher_yaml():
    return ExamplePatcherYaml


@pytest.fixture
def workflow_patcher_yaml(tmp_path: Path) -> Path:
    return tmp_path / ".workflow-patcher.yml"


@pytest.fixture
def workflow_patcher(workflow_patcher_yaml) -> WorkflowPatcher:
    return WorkflowPatcher(
        github_template_dict=PROJECT_CONFIG.github_template_dict,
        file_path=workflow_patcher_yaml,
    )


@pytest.fixture
def remove_job_yaml(example_patcher_yaml, workflow_patcher_yaml):
    content = cleandoc(example_patcher_yaml.remove_jobs)
    workflow_patcher_yaml.write_text(content)
    return content


@pytest.fixture
def step_customization_yaml(request, example_patcher_yaml, workflow_patcher_yaml):
    # request.param will hold the value passed from @pytest.mark.parametrize
    action_value = request.param

    text = example_patcher_yaml.step_customization.format(action=action_value)
    content = cleandoc(text)
    workflow_patcher_yaml.write_text(content)
    return content
