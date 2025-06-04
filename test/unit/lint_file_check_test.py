import json
import sqlite3
from pathlib import Path

import pytest

from exasol.toolbox.nox import _artifacts


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
    actual = _artifacts._is_valid_coverage(path)
    assert actual == expected
