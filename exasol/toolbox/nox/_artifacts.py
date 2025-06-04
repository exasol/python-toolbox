import json
import re
import shutil
import sqlite3
import sys
from collections.abc import Iterable
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import MINIMUM_PYTHON_VERSION
from noxconfig import PROJECT_CONFIG

COVERAGE_FILE = ".coverage"
COVERAGE_XML = "ci-coverage.xml"
LINT_JSON = ".lint.json"
LINT_TXT = ".lint.txt"
SECURITY_JSON = ".security.json"

ALL_FILES = {COVERAGE_FILE, LINT_JSON, LINT_TXT, SECURITY_JSON}

LINT_JSON_ATTRIBUTES = {
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


@nox.session(name="artifacts:validate", python=False)
def check_artifacts(session: Session) -> None:
    """Validate that all project artifacts are available and consistent"""
    if not_available := _missing_files(ALL_FILES, PROJECT_CONFIG.root):
        print(f"not available: {not_available}", file=sys.stderr)
        sys.exit(1)

    all_is_valid_checks = [
        _is_valid_lint_txt(Path(PROJECT_CONFIG.root, LINT_TXT)),
        _is_valid_lint_json(Path(PROJECT_CONFIG.root, LINT_JSON)),
        _is_valid_security_json(Path(PROJECT_CONFIG.root, SECURITY_JSON)),
        _is_valid_coverage(Path(PROJECT_CONFIG.root, COVERAGE_FILE)),
    ]

    if not all(all_is_valid_checks):
        sys.exit(1)


def _missing_files(expected_files: set, directory: Path) -> set:
    files = {f.name for f in directory.iterdir() if f.is_file()}
    return expected_files - files


def _print_validation_error(file: Path, message: str) -> None:
    print(f"error in [{file.name}]: {message}")


def _is_valid_lint_txt(file: Path) -> bool:
    content = file.read_text()
    expr = re.compile(r"^Your code has been rated at (\d+.\d+)/.*", re.MULTILINE)
    matches = expr.search(content)
    if not matches:
        _print_validation_error(file, "Could not find a rating")
        return False
    return True


def _is_valid_lint_json(file: Path) -> bool:
    try:
        content = file.read_text()
        issues = json.loads(content)
    except json.JSONDecodeError as ex:
        _print_validation_error(file, f"Invalid json file, details: {ex}")
        return False

    for number, issue in enumerate(issues):
        actual = set(issue.keys())
        missing = LINT_JSON_ATTRIBUTES - actual
        if len(missing) > 0:
            _print_validation_error(
                file,
                f"Invalid format, issue {number} is missing the following attributes {missing}",
            )
            return False
    return True


def _is_valid_security_json(file: Path) -> bool:
    try:
        content = file.read_text()
        actual = set(json.loads(content))
    except json.JSONDecodeError as ex:
        _print_validation_error(file, f"Invalid json file, details: {ex}")
        return False
    expected = {"errors", "generated_at", "metrics", "results"}
    missing = expected - actual
    if len(missing) > 0:
        _print_validation_error(
            file,
            f"Invalid format, the file is missing the following attributes {missing}",
        )
        return False
    return True


def _is_valid_coverage(path: Path) -> bool:
    try:
        conn = sqlite3.connect(path)
    except sqlite3.Error as ex:
        _print_validation_error(
            path, f"database connection not possible, details: {ex}"
        )
        return False
    cursor = conn.cursor()
    try:
        actual_tables = set(
            cursor.execute("select name from sqlite_schema where type == 'table'")
        )
    except sqlite3.Error as ex:
        _print_validation_error(path, f"schema query not possible, details: {ex}")
        return False
    expected = {"coverage_schema", "meta", "file", "line_bits"}
    actual = {f[0] for f in actual_tables if (f[0] in expected)}
    missing = expected - actual
    if len(missing) > 0:
        _print_validation_error(
            path,
            f"Invalid database, the database is missing the following tables {missing}",
        )
        return False
    return True


@nox.session(name="artifacts:copy", python=False)
def copy_artifacts(session: Session) -> None:
    """
    Copy artifacts to the current directory
    """

    artifact_dir = Path(session.posargs[0])
    suffix = _python_version_suffix()
    _combine_coverage(session, artifact_dir, f"coverage{suffix}*/{COVERAGE_FILE}")
    _copy_artifacts(
        artifact_dir,
        artifact_dir.parent,
        [
            f"lint{suffix}/{LINT_TXT}",
            f"lint{suffix}/{LINT_JSON}",
            f"security{suffix}/{SECURITY_JSON}",
        ],
    )


def _python_version_suffix() -> str:
    versions = getattr(PROJECT_CONFIG, "python_versions", None)
    pivot = versions[0] if versions else MINIMUM_PYTHON_VERSION
    return f"-python{pivot}"


def _combine_coverage(session: Session, artifact_dir: Path, pattern: str):
    """
    pattern: glob pattern, e.g. "*.coverage"
    """
    if args := [f for f in artifact_dir.glob(pattern) if f.exists()]:
        session.run("coverage", "combine", "--keep", *sorted(args))
    else:
        print(f"Could not find any file {artifact_dir}/{pattern}", file=sys.stderr)


def _copy_artifacts(source: Path, dest: Path, files: Iterable[str]):
    for file in files:
        path = source / file
        if path.exists():
            print(f"Copying file {path}", file=sys.stderr)
            shutil.copy(path, dest)
        else:
            print(f"File not found {path}", file=sys.stderr)


def _prepare_coverage_xml(session: Session, source: Path) -> None:
    command = ["coverage", "xml", "-o", COVERAGE_XML, "--include", f"{source}/*"]
    session.run(*command)


def _upload_to_sonar(session: Session, sonar_token: str) -> None:
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
    session.run(*command)


@nox.session(name="artifacts:sonar", python=False)
def upload_artifacts_to_sonar(session: Session) -> None:
    """Upload artifacts to sonar for analysis"""
    sonar_token = session.posargs[0]
    _prepare_coverage_xml(session, PROJECT_CONFIG.source)
    _upload_to_sonar(session, sonar_token)
