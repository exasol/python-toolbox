import pytest

from exasol.toolbox.tools import template


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
    "templates,pkg,expected",
    [
        (
            "all",
            "exasol.toolbox.templates.github.ISSUE_TEMPLATE",
            [
                "blank.md",
                "bug.md",
                "documentation.md",
                "feature.md",
                "refactoring.md",
                "security.md",
            ],
        ),
    ],
)
def test_install_templates(templates, pkg, expected, tmp_path):
    template.install_template(templates, tmp_path, pkg)
    actual = {file.name for file in tmp_path.iterdir()}
    expected = {name for name in expected}
    assert actual == expected
