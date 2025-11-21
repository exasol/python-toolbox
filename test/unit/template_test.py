import pytest

from exasol.toolbox.tools import template


def test_retrieve_workflow_templates():
    subpackage = "exasol.toolbox.templates.github.workflows"
    expected = {
        "build-and-publish": "build-and-publish.yml",
        "cd": "cd.yml",
        "check-release-tag": "check-release-tag.yml",
        "checks": "checks.yml",
        "ci": "ci.yml",
        "gh-pages": "gh-pages.yml",
        "matrix-all": "matrix-all.yml",
        "matrix-exasol": "matrix-exasol.yml",
        "matrix-python": "matrix-python.yml",
        "merge-gate": "merge-gate.yml",
        "pr-merge": "pr-merge.yml",
        "report": "report.yml",
        "slow-checks": "slow-checks.yml",
    }
    actual = template._templates(subpackage)
    actual = {name: path.name for name, path in actual.items()}
    assert actual == expected


def test_retrieve_issue_templates():
    subpackage = "exasol.toolbox.templates.github.ISSUE_TEMPLATE"
    expected = {
        "blank": "blank.md",
        "bug": "bug.md",
        "documentation": "documentation.md",
        "feature": "feature.md",
        "refactoring": "refactoring.md",
        "security": "security.md",
    }
    actual = template._templates(subpackage)
    actual = {name: path.name for name, path in actual.items()}
    assert actual == expected


@pytest.mark.parametrize(
    "subpackage,expected",
    [
        (
            "exasol.toolbox.templates.github.workflows",
            {
                "build-and-publish": "build-and-publish.yml",
                "cd": "cd.yml",
                "check-release-tag": "check-release-tag.yml",
                "checks": "checks.yml",
                "ci": "ci.yml",
                "gh-pages": "gh-pages.yml",
                "matrix-all": "matrix-all.yml",
                "matrix-exasol": "matrix-exasol.yml",
                "matrix-python": "matrix-python.yml",
                "merge-gate": "merge-gate.yml",
                "pr-merge": "pr-merge.yml",
                "report": "report.yml",
                "slow-checks": "slow-checks.yml",
            },
        ),
        (
            "exasol.toolbox.templates.github.ISSUE_TEMPLATE",
            {
                "blank": "blank.md",
                "bug": "bug.md",
                "documentation": "documentation.md",
                "feature": "feature.md",
                "refactoring": "refactoring.md",
                "security": "security.md",
            },
        ),
    ],
)
def test_retrieve_templates(subpackage, expected):
    actual = template._templates(subpackage)
    actual = {name: path.name for name, path in actual.items()}
    assert actual == expected


@pytest.mark.parametrize(
    "templates,pkg,template_type,expected",
    [
        (
            "all",
            "exasol.toolbox.templates.github.ISSUE_TEMPLATE",
            "issue",
            [
                "blank.md",
                "bug.md",
                "documentation.md",
                "feature.md",
                "refactoring.md",
                "security.md",
            ],
        ),
        (
            "all",
            "exasol.toolbox.templates.github.workflows",
            "workflow",
            [
                "build-and-publish.yml",
                "cd.yml",
                "check-release-tag.yml",
                "checks.yml",
                "ci.yml",
                "gh-pages.yml",
                "matrix-all.yml",
                "matrix-exasol.yml",
                "matrix-python.yml",
                "merge-gate.yml",
                "pr-merge.yml",
                "report.yml",
                "slow-checks.yml",
            ],
        ),
    ],
)
def test_install_templates(templates, pkg, template_type, expected, tmp_path):
    template.install_template(templates, tmp_path, pkg, template_type)
    actual = {file.name for file in tmp_path.iterdir()}
    expected = {name for name in expected}
    assert actual == expected
