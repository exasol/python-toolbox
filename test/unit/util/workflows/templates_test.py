from exasol.toolbox.util.workflows.templates import get_workflow_templates


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
