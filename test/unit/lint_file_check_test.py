import json

import pytest
from pathlib import Path
import sqlite3

from exasol.toolbox.nox import _gh

@pytest.mark.parametrize(
    "files,requested_files,expected",
    [
        (
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            []
        ), (
            [".lint.txt", ".security.json", ".coverage"],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            [".lint.json"]
        ), (
            [".lint.json", ".security.json", ".coverage"],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            [".lint.txt"]
        ), (
            [".lint.json", ".lint.txt", ".coverage"],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            [".security.json"]
        ), (
            [".lint.json", ".lint.txt", ".security.json"],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            [".coverage"]
        ), (
            [],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            [".lint.json", ".lint.txt", ".security.json", ".coverage"]
        ),
    ]
)
def test_check_lint_files(files, requested_files, expected, tmp_path):
    path = Path(tmp_path)
    for file in files:
        Path(path, file).touch()

    actual = _gh.files_not_available(requested_files, path)
    assert actual == expected


@pytest.mark.parametrize(
    "attributes,expected",
    [
        (
            ["type", "module", "obj", "line", "column", "endLine",
                "endColumn", "path", "symbol", "message", "message-id"],
            ""
        ),  (
            ["module", "obj", "line", "column", "endLine",
                "endColumn", "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "obj", "line", "column", "endLine",
             "endColumn", "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "line", "column", "endLine",
             "endColumn", "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "column", "endLine",
             "endColumn", "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "endLine",
             "endColumn", "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "column",
             "endColumn", "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "column", "endLine",
             "path", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "column", "endLine",
             "endColumn", "symbol", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "column", "endLine",
             "endColumn", "path", "message", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "column", "endLine",
             "endColumn", "path", "symbol", "message-id"],
            "incompatible format"
        ),  (
            ["type", "module", "obj", "line", "column", "endLine",
             "endColumn", "path", "symbol", "message"],
            "incompatible format"
        ),
    ]
)
def test_check_lint_json(attributes, expected, tmp_path):
    path = Path(tmp_path, ".lint.json")
    path.touch()
    attributes_dict = {}
    for attribute in attributes:
        attributes_dict[attribute] = None
    with path.open("w") as file:
        json.dump([attributes_dict], file)
    actual = _gh.check_lint_json(path.parent)
    assert actual == expected


@pytest.mark.parametrize(
    "attributes,expected",
    [
        (['errors', 'generated_at', 'metrics', 'results'], ""),
        (["generated_at", "metrics", "results"], "incompatible format"),
        (["errors", "metrics", "results"], "incompatible format"),
        (["errors", "generated_at", "results"], "incompatible format"),
        (["errors", "generated_at", "metrics"], "incompatible format"),
    ]
)
def test_check_lint_json(attributes, expected, tmp_path):
    path = Path(tmp_path, ".security.json")
    path.touch()
    attributes_dict = {}
    for attribute in attributes:
        attributes_dict[attribute] = None
    with path.open("w") as file:
        json.dump(attributes_dict, file)
    actual = _gh.check_security_json(path.parent)
    assert actual == expected


@pytest.mark.parametrize(
    "tables, expected",
    [
        (["coverage_schema", "meta", "file", "line_bits"], ""),
        (["meta", "file", "line_bits"], "not existing tables: ['coverage_schema']"),
        (["coverage_schema", "file", "line_bits"], "not existing tables: ['meta']"),
        (["coverage_schema", "meta", "line_bits"], "not existing tables: ['file']"),
        (["coverage_schema", "meta", "file", ], "not existing tables: ['line_bits']"),
    ]
)
def test_check_coverage(tables, expected, tmp_path):
    path = Path(tmp_path, ".coverage")
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (test INTEGER)")
    actual = _gh.check_coverage(path.parent)
    assert actual == expected
