import json

import pytest

from exasol.toolbox.tools import lint


@pytest.mark.parametrize(
    "data",
    [
        {
            "type": "test_type",
            "module": "test_module",
            "obj": "test_obj",
            "line": 0,
            "column": 1,
            "endLine": 2,
            "endColumn": 3,
            "path": "test_path",
            "symbol": "test_symbol",
            "message": "test_message",
            "message-id": "test_message_id",
        },
    ],
)
def test_lint_issue_from_json(data):
    actual = lint.lint_issue_from_json(json.dumps([data]))
    expected = lint.LintIssue(
        type=data["type"],
        module=data["module"],
        obj=data["obj"],
        line=data["line"],
        column=data["column"],
        endLine=data["endLine"],
        endColumn=data["endColumn"],
        path=data["path"],
        symbol=data["symbol"],
        message=data["message"],
        message_id=data["message-id"],
    )
    assert list(actual) == [expected]


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "type": "test_type",
                "module": "test_module",
                "obj": "test_obj",
                "line": 0,
                "column": 1,
                "endLine": 2,
                "endColumn": 3,
                "path": "test_path",
                "symbol": "test_symbol",
                "message": "test_message",
                "message-id": "test_message_id",
            },
            """# Static Code Analysis

|File|line<br>column|id|message|
|---|:-:|:-:|---|
|test_path|line: 0<br>column: 1|test_message_id|test_message|
""",
        )
    ],
)
def test_lint_issue_to_markdown(data, expected):
    issue = lint.LintIssue(
        type=data["type"],
        module=data["module"],
        obj=data["obj"],
        line=data["line"],
        column=data["column"],
        endLine=data["endLine"],
        endColumn=data["endColumn"],
        path=data["path"],
        symbol=data["symbol"],
        message=data["message"],
        message_id=data["message-id"],
    )
    issues = [issue]
    actual = lint.lint_issue_to_markdown(issues)
    assert actual == expected
