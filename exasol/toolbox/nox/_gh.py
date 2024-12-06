import nox
from nox import Session
from noxconfig import PROJECT_CONFIG
import sys
from pathlib import Path
import json
import sqlite3
from typing import Iterable


@nox.session(name="check:lint-files", python=False)
def check_lint_files(session: Session) -> None:
    """task to validate linting files"""
    if not_available := files_not_available(
            [".lint.json", ".lint.txt", ".security.json", ".coverage"],
            PROJECT_CONFIG.root):
        print(f"not available: {not_available}")
        sys.exit(1)

    error = False
    if msg := check_lint_json(PROJECT_CONFIG.root):
        print(f"error in [.lint.json]: {msg}")
        error = True
    if msg := check_security_json(PROJECT_CONFIG.root):
        print(f"error in [.security.json]: {msg}")
        error = True
    if msg := check_coverage(PROJECT_CONFIG.root):
        print(f"error in [.coverage]: {msg}")
        error = True
    if error:
        sys.exit(1)


def files_not_available(requested: list, path: Path) -> list:
    not_existing_files = requested.copy()
    for file in path.iterdir():
        if file.is_file():
            if file.name in not_existing_files:
                not_existing_files.remove(file.name)
    return not_existing_files


def check_lint_json(path: Path) -> str:
    path = Path(path, ".lint.json")
    try:
        with path.open("r") as file:
            issues = json.load(file)
            error = False
            for issue in issues:
                attributes = ["type", "module", "obj", "line", "column", "endLine",
                              "endColumn", "path", "symbol", "message", "message-id"]
                for attribute in attributes:
                    error |= attribute not in issue
            if error:
                return "incompatible format"
            return ""

    except json.JSONDecodeError:
        return "parsing of json not possible"


def check_security_json(path: Path) -> str:
    path = Path(path, ".security.json")
    try:
        with path.open("r") as input_file:
            json_file = json.load(input_file)
            error = False
            attributes = ["errors", "generated_at", "metrics", "results"]
            for attribute in attributes:
                error |= attribute not in json_file
            if error:
                return "incompatible format"
            return ""

    except json.JSONDecodeError:
        return "parsing of json not possible"


def check_coverage(path: Path) -> str:
    path = Path(path, ".coverage")
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        not_existing_tables = ["coverage_schema", "meta", "file", "line_bits"]
        data = cursor.execute("select name from sqlite_schema where type == 'table'")
        for row in data:
            if row[0] in not_existing_tables:
                not_existing_tables.remove(row[0])
        conn.close()
        if not_existing_tables:
            return "not existing tables: " + str(not_existing_tables)
        return ""
    except sqlite3.Error:
        return "connection to database not possible"
