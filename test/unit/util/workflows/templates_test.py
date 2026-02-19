from exasol.toolbox.util.workflows.templates import get_workflow_templates
from noxconfig import PROJECT_CONFIG


def test_get_workflow_templates():
    result = get_workflow_templates()

    assert result.keys() == {
        "build-and-publish",
        "cd",
        "check-release-tag",
        "checks",
        "ci",
        "gh-pages",
        "matrix-all",
        "matrix-exasol",
        "matrix-python",
        "merge-gate",
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
