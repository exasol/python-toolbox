import pytest

from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowNameError,
    NotMaintainedWorkflowError,
)
from exasol.toolbox.util.workflows.templates import (
    NOT_MAINTAINED_WORKFLOW_NAMES,
    WORKFLOW_TEMPLATE_OPTIONS,
    get_workflow_templates,
    validate_workflow_name,
)
from noxconfig import PROJECT_CONFIG


def test_get_workflow_templates(project_config):
    result = get_workflow_templates()

    assert result.keys() == {
        "build-and-publish",
        "cd",
        "check-release-tag",
        "checks",
        "ci",
        "fast-tests",
        "dependency-update",
        "gh-pages",
        "matrix-all",
        "matrix-exasol",
        "matrix-python",
        "merge-gate",
        "periodic-validation",
        "pr-merge",
        "report",
        "slow-checks",
    }
    # check only one path, as all formatted the same by convention
    assert (
        result["build-and-publish"]
        == PROJECT_CONFIG.source_code_path
        / "templates"
        / "github"
        / "workflows"
        / "build-and-publish.yml"
    )


class TestValidateWorkflowName:
    @staticmethod
    @pytest.mark.parametrize(
        "workflow_name",
        WORKFLOW_TEMPLATE_OPTIONS.keys() - set(NOT_MAINTAINED_WORKFLOW_NAMES),
    )
    def test_returns_valid_maintained_names(workflow_name):
        name = validate_workflow_name(workflow_name)
        assert name == workflow_name

    @staticmethod
    def test_rejects_unknown_workflow():
        with pytest.raises(InvalidWorkflowNameError, match="Invalid workflow: unknown"):
            validate_workflow_name("unknown")

    @staticmethod
    def test_rejects_not_maintained_workflow():
        with pytest.raises(NotMaintainedWorkflowError, match="PTB-seeded workflow"):
            validate_workflow_name(NOT_MAINTAINED_WORKFLOW_NAMES[0])
