import pytest
from ruamel.yaml import CommentedMap

from exasol.toolbox.util.workflows.exceptions import (
    YamlJobValueError,
    YamlStepIdValueError,
)
from exasol.toolbox.util.workflows.patch_workflow import ActionType
from exasol.toolbox.util.workflows.process_template import WorkflowModifier
from exasol.toolbox.util.workflows.render_yaml import YamlRenderer
from noxconfig import PROJECT_CONFIG

WORKFLOW_YAML = """
name: Checks

on:
  workflow_call:

jobs:
  build-documentation-and-check-links:
    name: Docs
    runs-on: "ubuntu-24.04"
    permissions:
      contents: read
    steps:
      - name: Check out Repository
        id: check-out-repository
        uses: actions/checkout@v6

  run-unit-tests:
    name: Run Unit Tests (Python-${{ matrix.python-versions }})
    runs-on: "ubuntu-24.04"
    permissions:
      contents: read
    strategy:
      fail-fast: false
      matrix:
        python-versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]

    steps:
      - name: Check out Repository
        id: check-out-repository
        uses: actions/checkout@v6

"""


@pytest.fixture
def workflow_name():
    return "checks"


@pytest.fixture
def checks_yaml(tmp_path, workflow_name):
    file_path = tmp_path / workflow_name
    file_path.write_text(WORKFLOW_YAML)
    return file_path


@pytest.fixture
def workflow_dict(checks_yaml) -> CommentedMap:
    return YamlRenderer(
        github_template_dict=PROJECT_CONFIG.github_template_dict, file_path=checks_yaml
    ).get_yaml_dict()


class TestWorkflowModifier:
    @staticmethod
    def test__remove_jobs_works(
        workflow_name, workflow_dict, workflow_patcher, remove_job_yaml
    ):
        workflow_modifier = WorkflowModifier(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        result = workflow_modifier.get_patched_workflow()

        # The original was not altered as it was deepcopied before modifications.
        assert list(workflow_dict["jobs"].keys()) == [
            "build-documentation-and-check-links",
            "run-unit-tests",
        ]
        # The original and resulting workflows should have the same values here.
        assert result["name"] == workflow_dict["name"]
        assert result["on"] == workflow_dict["on"]
        assert (
            result["jobs"]["run-unit-tests"] == workflow_dict["jobs"]["run-unit-tests"]
        )
        # The resulting workflow has job "build-documentation-and-check-links" removed.
        assert list(result["jobs"].keys()) == ["run-unit-tests"]

    @staticmethod
    @pytest.mark.parametrize(
        "step_customization_yaml",
        [ActionType.REPLACE.value],
        indirect=True,
    )
    def test__customize_steps_replacement_works(
        workflow_name, workflow_dict, workflow_patcher, step_customization_yaml
    ):
        workflow_modifier = WorkflowModifier(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        result = workflow_modifier.get_patched_workflow()

        # The original and resulting workflows should have the same values here.
        assert result["name"] == workflow_dict["name"]
        assert result["on"] == workflow_dict["on"]
        assert list(result["jobs"].keys()) == list(workflow_dict["jobs"].keys())
        assert (
            result["jobs"]["build-documentation-and-check-links"]
            == workflow_dict["jobs"]["build-documentation-and-check-links"]
        )
        # The replaced step operation was done in job `run-unit-tests` for step
        # `check-out-repository`. The replacement was mostly identical to the original
        # value, but it has a `with`.
        assert result["jobs"]["run-unit-tests"]["steps"][0].pop("with") == CommentedMap(
            {"fetch-depth": 0}
        )
        # Without the `with`, they should be the same, as that's how the test is set up.
        assert (
            result["jobs"]["run-unit-tests"] == workflow_dict["jobs"]["run-unit-tests"]
        )

    @staticmethod
    @pytest.mark.parametrize(
        "step_customization_yaml",
        [ActionType.INSERT_AFTER.value],
        indirect=True,
    )
    def test__customize_steps_insertion_after_works(
        workflow_name, workflow_dict, workflow_patcher, step_customization_yaml
    ):
        workflow_modifier = WorkflowModifier(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        result = workflow_modifier.get_patched_workflow()

        # The original and internal workflows should have the same values here.
        assert result["name"] == workflow_dict["name"]
        assert result["on"] == workflow_dict["on"]
        assert (
            result["jobs"]["build-documentation-and-check-links"]
            == workflow_dict["jobs"]["build-documentation-and-check-links"]
        )
        # The insert after job added a step at the end of `run-unit-tests`.
        assert (
            len(result["jobs"]["run-unit-tests"]["steps"])
            == len(workflow_dict["jobs"]["run-unit-tests"]["steps"]) + 1
            == 2
        )
        assert (
            result["jobs"]["run-unit-tests"]["steps"][0]
            == workflow_dict["jobs"]["run-unit-tests"]["steps"][0]
        )
        # The inserted after was done in job `run-unit-tests`, after step
        # `check-out-repository`. It has a `with` but is otherwise identical to
        # the preceding step.
        assert result["jobs"]["run-unit-tests"]["steps"][1].pop("with") == CommentedMap(
            {"fetch-depth": 0}
        )
        assert (
            result["jobs"]["run-unit-tests"]["steps"][1]
            == result["jobs"]["run-unit-tests"]["steps"][0]
        )


class TestWorkflowModifierExceptions:
    @staticmethod
    def test_job_does_not_exist_raises_exception(
        workflow_name, workflow_dict, workflow_patcher, remove_job_yaml
    ):
        # Remove job that would be otherwise removed by the WorkflowModifier
        job_name = "build-documentation-and-check-links"
        workflow_dict["jobs"].pop(job_name)

        workflow_modifier = WorkflowModifier(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        with pytest.raises(YamlJobValueError, match=job_name):
            workflow_modifier.get_patched_workflow()

    @staticmethod
    @pytest.mark.parametrize(
        "step_customization_yaml",
        [ActionType.REPLACE.value],
        indirect=True,
    )
    def test_step_id_does_not_exist_raises_exception(
        workflow_name, workflow_dict, workflow_patcher, step_customization_yaml
    ):
        # Remove step_id that would be otherwise replaced by the WorkflowModifier
        job_name = "run-unit-tests"
        step_id = "check-out-repository"
        step = workflow_dict["jobs"][job_name]["steps"].pop(0)
        assert step["id"] == step_id

        workflow_modifier = WorkflowModifier(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        with pytest.raises(YamlStepIdValueError, match=step_id):
            workflow_modifier.get_patched_workflow()
