from pathlib import Path
import os
import pytest

from exasol.toolbox.tools import template


def test_retrieve_workflow_templates():
    subpackage = "exasol.toolbox.templates.github.workflows"
    expected = {
        "build-and-publish": "build-and-publish.yml",
        "check-release-tag": "check-release-tag.yml",
        "checks": "checks.yml",
        "ci-cd": "ci-cd.yml",
        "ci": "ci.yml",
        "gh-pages": "gh-pages.yml",
        "pr-merge": "pr-merge.yml",
        "report": "report.yml",
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
                    "check-release-tag": "check-release-tag.yml",
                    "checks": "checks.yml",
                    "ci-cd": "ci-cd.yml",
                    "ci": "ci.yml",
                    "gh-pages": "gh-pages.yml",
                    "pr-merge": "pr-merge.yml",
                    "report": "report.yml",
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
                "check-release-tag.yml",
                "checks.yml",
                "ci-cd.yml",
                "ci.yml",
                "gh-pages.yml",
                "pr-merge.yml",
                "report.yml",
            ],
        ),
    ]
)
def test_install_templates(templates, pkg, template_type, expected, tmp_path):
    template.install_template(templates, Path(tmp_path), pkg, template_type)
    error = False
    for name in expected:
        if os.path.exists(f"{tmp_path}/{name}"):
            os.remove(f"{tmp_path}/{name}")
        else:
            print(f"{tmp_path}/{name}")
            error = True
    assert not error
