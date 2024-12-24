import json
import pathlib
import re
import sqlite3
import sys
from pathlib import Path

import nox
from nox import Session

from noxconfig import PROJECT_CONFIG


@nox.session(name="artifacts:validate", python=False)
def check_artifacts(session: Session) -> None:
    """Validate that all project artifacts are available and consistent"""
    if not_available := _missing_files(
        {".lint.txt", ".security.json", ".coverage"}, PROJECT_CONFIG.root
    ):
        print(f"not available: {not_available}")
        sys.exit(1)

    error = False
    if msg := _validate_lint_txt(Path(PROJECT_CONFIG.root, ".lint.txt")):
        print(f"error in [.lint.txt]: {msg}")
    if msg := _validate_lint_json(Path(PROJECT_CONFIG.root, ".lint.json")):
        print(f"error in [.lint.json]: {msg}")
    if msg := _validate_security_json(Path(PROJECT_CONFIG.root, ".security.json")):
        print(f"error in [.security.json]: {msg}")
        error = True
    if msg := _validate_coverage(Path(PROJECT_CONFIG.root, ".coverage")):
        print(f"error in [.coverage]: {msg}")
        error = True
    if error:
        sys.exit(1)


def _missing_files(expected_files: set, directory: Path) -> set:
    files = {f.name for f in directory.iterdir() if f.is_file()}
    return expected_files - files


def _validate_lint_txt(file: Path) -> str:
    try:
        content = file.read_text()
    except FileNotFoundError as ex:
        return f"Could not find file {file}, details: {ex}"
    expr = re.compile(r"^Your code has been rated at (\d+.\d+)/.*", re.MULTILINE)
    matches = expr.search(content)
    if not matches:
        return f"Could not find a rating"
    return ""


def _validate_lint_json(file: Path) -> str:
    try:
        content = file.read_text()
    except FileNotFoundError as ex:
        return f"Could not find file {file}, details: {ex}"
    try:
        issues = json.loads(content)
    except json.JSONDecodeError as ex:
        return f"Invalid json file, details: {ex}"
    expected = {
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
    }
    for number, issue in enumerate(issues):
        actual = set(issue.keys())
        missing = expected - actual
        if len(missing) > 0:
            return f"Invalid format, issue {number} is missing the following attributes {missing}"
    return ""


def _validate_security_json(file: Path) -> str:
    try:
        content = file.read_text()
    except FileNotFoundError as ex:
        return f"Could not find file {file}, details: {ex}"
    try:
        actual = set(json.loads(content))
    except json.JSONDecodeError as ex:
        return f"Invalid json file, details: {ex}"
    expected = {"errors", "generated_at", "metrics", "results"}
    missing = expected - actual
    if len(missing) > 0:
        return f"Invalid format, the file is missing the following attributes {missing}"
    return ""


def _validate_coverage(path: Path) -> str:
    try:
        conn = sqlite3.connect(path)
    except sqlite3.Error as ex:
        return f"database connection not possible, details: {ex}"
    cursor = conn.cursor()
    try:
        actual_tables = set(
            cursor.execute("select name from sqlite_schema where type == 'table'")
        )
    except sqlite3.Error as ex:
        return f"schema query not possible, details: {ex}"
    expected = {"coverage_schema", "meta", "file", "line_bits"}
    actual = {f[0] for f in actual_tables if (f[0] in expected)}
    missing = expected - actual
    if len(missing) > 0:
        return (
            f"Invalid database, the database is missing the following tables {missing}"
        )
    return ""
