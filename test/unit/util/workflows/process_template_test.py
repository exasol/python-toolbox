import pytest
from ruamel.yaml import CommentedMap

from exasol.toolbox.util.workflows.patch_workflow import ActionType
from exasol.toolbox.util.workflows.process_template import WorkflowPatcher
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
    return "checks.yml"


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
    def test__remove_jobs(
        workflow_name, workflow_dict, workflow_patcher, remove_job_yaml
    ):
        workflow_patcher = WorkflowPatcher(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        result = workflow_patcher.get_patched_workflow()

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
    def test__customize_steps_replacement(
        workflow_name, workflow_dict, workflow_patcher, step_customization_yaml
    ):
        workflow_patcher = WorkflowPatcher(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        result = workflow_patcher.get_patched_workflow()

        # The original and resulting workflows should have the same values here.
        assert result["name"] == workflow_dict["name"]
        assert result["on"] == workflow_dict["on"]
        assert list(result["jobs"].keys()) == list(workflow_dict["jobs"].keys())
        assert (
            result["jobs"]["build-documentation-and-check-links"]
            == workflow_dict["jobs"]["build-documentation-and-check-links"]
        )
        # The replaced step (in job `run-unit-tests`, at step `check-out-repository`)
        # has a `with`.
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
    def test__customize_steps_insertion_after(
        workflow_name, workflow_dict, workflow_patcher, step_customization_yaml
    ):
        workflow_patcher = WorkflowPatcher(
            workflow_dict=workflow_dict,
            patch_yaml=workflow_patcher.extract_by_workflow(workflow_name),
        )

        result = workflow_patcher.get_patched_workflow()

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
        # The inserted after was done after step (in job `run-unit-tests`, at step
        # `check-out-repository`). It has a `with` but is otherwise identical to
        # the preceding step.
        assert result["jobs"]["run-unit-tests"]["steps"][1].pop("with") == CommentedMap(
            {"fetch-depth": 0}
        )
        assert (
            result["jobs"]["run-unit-tests"]["steps"][1]
            == result["jobs"]["run-unit-tests"]["steps"][0]
        )
