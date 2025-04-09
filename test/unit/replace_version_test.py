import pytest

from exasol.toolbox.tools.replace_version import (
    _update_line_with_version,
    update_versions,
)


@pytest.mark.parametrize(
    "line,expected",
    [
        pytest.param(
            "exasol/python-toolbox/.github/actions/python-environment@1.0.0",
            "exasol/python-toolbox/.github/actions/python-environment@2.0.0",
            id="github_action",
        ),
        pytest.param(
            "pip install exasol-toolbox==1.0.0\n",
            "pip install exasol-toolbox==2.0.0\n",
            id="pypi_version",
        ),
        pytest.param(
            "- name: Create Security Issue Report",
            "- name: Create Security Issue Report",
            id="no_change_expected",
        ),
    ],
)
def test_update_line_with_version(line: str, expected: str):
    actual = _update_line_with_version(line=line, version="2.0.0")
    assert actual == expected


@pytest.mark.parametrize(
    "line_to_change, expected",
    [
        pytest.param(
            "exasol/python-toolbox/.github/actions/python-environment@1.0.0",
            "exasol/python-toolbox/.github/actions/python-environment@2.0.0",
            id="github_action",
        ),
        pytest.param(
            "pip install exasol-toolbox==1.0.0\n",
            "pip install exasol-toolbox==2.0.0\n",
            id="pypi_version",
        ),
    ],
)
def test_update_versions(line_to_change, expected):
    dummy_lines = [
        "exasol/python-toolbox/.github/actions/python-environment@dummy\n",
        "- name: Create Security Issue Report\n",
        "pip install exasol-toolbox==dummy\n",
    ]
    lines = dummy_lines + [line_to_change]
    expected_lines = dummy_lines + [expected]

    actual = update_versions(lines=lines, version="2.0.0")
    assert actual == expected_lines
