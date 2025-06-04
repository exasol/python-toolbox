import json
import re
import shutil
import sqlite3
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import MINIMUM_PYTHON_VERSION
from noxconfig import PROJECT_CONFIG

COVERAGE_XML = "ci-coverage.xml"
LINT_JSON = ".lint.json"
SECURITY_JSON = ".security.json"


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
    if msg := _validate_lint_json(Path(PROJECT_CONFIG.root, LINT_JSON)):
        print(f"error in [.lint.json]: {msg}")
    if msg := _validate_security_json(Path(PROJECT_CONFIG.root, SECURITY_JSON)):
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


@nox.session(name="artifacts:copy", python=False)
def copy_artifacts(session: Session) -> None:
    """
    Copy artifacts to the current directory
    """

    dir = Path(session.posargs[0])
    suffix = _python_version_suffix()
    _combine_coverage(session, dir, f"coverage{suffix}*/.coverage")
    _copy_artifacts(
        dir,
        dir.parent,
        [
            f"lint{suffix}/.lint.txt",
            f"lint{suffix}/.lint.json",
            f"security{suffix}/.security.json",
        ],
    )


def _python_version_suffix() -> str:
    versions = getattr(PROJECT_CONFIG, "python_versions", None)
    pivot = versions[0] if versions else MINIMUM_PYTHON_VERSION
    return f"-python{pivot}"


def _combine_coverage(session: Session, dir: Path, pattern: str):
    """
    pattern: glob pattern, e.g. "*.coverage"
    """
    if args := [f for f in dir.glob(pattern) if f.exists()]:
        session.run("coverage", "combine", "--keep", *sorted(args))
    else:
        print(f"Could not find any file {dir}/{pattern}", file=sys.stderr)


def _copy_artifacts(source: Path, dest: Path, files: Iterable[str]):
    for file in files:
        path = source / file
        if path.exists():
            print(f"Copying file {path}", file=sys.stderr)
            shutil.copy(path, dest)
        else:
            print(f"File not found {path}", file=sys.stderr)


def _prepare_coverage_xml(source: Path) -> None:
    command = ["coverage", "xml", "-o", COVERAGE_XML, "--include", f"{source}/*"]
    subprocess.run(command, check=True)


def _upload_to_sonar(sonar_token: str) -> None:
    command = [
        "pysonar",
        "--sonar-token",
        sonar_token,
        "--sonar-python-coverage-report-paths",
        COVERAGE_XML,
        "--sonar-python-pylint-report-path",
        LINT_JSON,
        "--sonar-python-bandit-report-paths",
        SECURITY_JSON,
    ]
    subprocess.run(command, check=True)


@nox.session(name="artifacts:sonar", python=False)
def upload_artifacts_to_sonar(session: Session) -> None:
    """Upload artifacts to sonar for analysis"""
    sonar_token = session.posargs[0]
    _prepare_coverage_xml(PROJECT_CONFIG.source)
    _upload_to_sonar(sonar_token)
