import json
import sqlite3
from pathlib import Path

import pytest

from exasol.toolbox.nox import _artifacts


@pytest.mark.parametrize(
    "file,expected",
    [
        ("Your code has been rated at 7.85/10 (previous run: 7.83/10, +0.02", ""),
        (
            "test_text\nYour code has been rated at 7.85/10 (previous run: 7.83/10, +0.02\ntest_text",
            "",
        ),
        ("", "Could not find a rating"),
        ("test_text", "Could not find a rating"),
    ],
)
def test_check_lint_txt(file, expected, tmp_path):
    path = Path(tmp_path, ".lint.txt")
    path.touch()
    path.write_text(file)
    actual = _artifacts._validate_lint_txt(path)
    assert actual == expected


@pytest.mark.parametrize(
    "attributes,expected",
    [
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "",
        ),
        (
            [
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'type'}",
        ),
        (
            [
                "type",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'module'}",
        ),
        (
            [
                "type",
                "module",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'obj'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'line'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'column'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endColumn",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'endLine'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "path",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'endColumn'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "symbol",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'path'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "message",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'symbol'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message-id",
            ],
            "Invalid format, issue 0 is missing the following attributes {'message'}",
        ),
        (
            [
                "type",
                "module",
                "obj",
                "line",
                "column",
                "endLine",
                "endColumn",
                "path",
                "symbol",
                "message",
            ],
            "Invalid format, issue 0 is missing the following attributes {'message-id'}",
        ),
    ],
)
def test_check_lint_json(attributes, expected, tmp_path):
    path = Path(tmp_path, ".lint.json")
    path.touch()
    attributes_dict = {}
    for attribute in attributes:
        attributes_dict[attribute] = None
    with path.open("w") as file:
        json.dump([attributes_dict], file)
    actual = _artifacts._validate_lint_json(path)
    assert actual == expected


@pytest.mark.parametrize(
    "attributes,expected",
    [
        (["errors", "generated_at", "metrics", "results"], ""),
        (
            ["generated_at", "metrics", "results"],
            "Invalid format, the file is missing the following attributes {'errors'}",
        ),
        (
            ["errors", "metrics", "results"],
            "Invalid format, the file is missing the following attributes {'generated_at'}",
        ),
        (
            ["errors", "generated_at", "results"],
            "Invalid format, the file is missing the following attributes {'metrics'}",
        ),
        (
            ["errors", "generated_at", "metrics"],
            "Invalid format, the file is missing the following attributes {'results'}",
        ),
    ],
)
def test_check_security_json(attributes, expected, tmp_path):
    path = Path(tmp_path, ".security.json")
    path.touch()
    attributes_dict = {}
    for attribute in attributes:
        attributes_dict[attribute] = None
    with path.open("w") as file:
        json.dump(attributes_dict, file)
    actual = _artifacts._validate_security_json(path)
    assert actual == expected


@pytest.mark.parametrize(
    "tables, expected",
    [
        (["coverage_schema", "meta", "file", "line_bits"], ""),
        (
            ["meta", "file", "line_bits"],
            "Invalid database, the database is missing the following tables {'coverage_schema'}",
        ),
        (
            ["coverage_schema", "file", "line_bits"],
            "Invalid database, the database is missing the following tables {'meta'}",
        ),
        (
            ["coverage_schema", "meta", "line_bits"],
            "Invalid database, the database is missing the following tables {'file'}",
        ),
        (
            [
                "coverage_schema",
                "meta",
                "file",
            ],
            "Invalid database, the database is missing the following tables {'line_bits'}",
        ),
    ],
)
def test_check_coverage(tables, expected, tmp_path):
    path = Path(tmp_path, ".coverage")
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (test INTEGER)")
    actual = _artifacts._validate_coverage(path)
    assert actual == expected
