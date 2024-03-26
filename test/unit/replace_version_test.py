import pytest
from exasol.toolbox.tools import replace_version

@pytest.mark.parametrize(
    "line,replace_filter,version,expected", 
    [
        (
            ["line@0.0.0\n"],
            "line",
            "9.9.9",
            ["line@9.9.9\n"]
        ),
        (
            ["path/file@0.0.0\n"],
            "line",
            "9.9.9",
            ["path/file@0.0.0\n"]
        ),
        (
            ["path/file@1.2.3\n"],
            "path/file",
            "8.9.7",
            ["path/file@8.9.7\n"]
        )
    ]
)
def test_retrieve_issue_templates(line, replace_filter, version, expected):
    actual = replace_version._replace_version(line, replace_filter, version)
    assert actual == expected
