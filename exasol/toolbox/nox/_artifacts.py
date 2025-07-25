import json
import os
import re
import shutil
import sqlite3
import subprocess  # nosec
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

import nox
from nox import Session

from exasol.toolbox.nox._shared import MINIMUM_PYTHON_VERSION
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)

COVERAGE_DB = ".coverage"
COVERAGE_XML = "ci-coverage.xml"
LINT_JSON = ".lint.json"
LINT_TXT = ".lint.txt"
SECURITY_JSON = ".security.json"

ALL_LINT_FILES = {COVERAGE_DB, LINT_JSON, LINT_TXT, SECURITY_JSON}
COVERAGE_TABLES = {"coverage_schema", "meta", "file", "line_bits"}
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

SECURITY_JSON_ATTRIBUTES = {"errors", "generated_at", "metrics", "results"}


@nox.session(name="artifacts:validate", python=False)
def check_artifacts(session: Session) -> None:
    """Validate that all project artifacts are available and consistent"""
    all_files = {f.name for f in PROJECT_CONFIG.root.iterdir() if f.is_file()}
    if missing_files := (ALL_LINT_FILES - all_files):
        print(f"files not available: {missing_files}", file=sys.stderr)
        sys.exit(1)

    all_is_valid_checks = [
        _is_valid_lint_txt(Path(PROJECT_CONFIG.root, LINT_TXT)),
        _is_valid_lint_json(Path(PROJECT_CONFIG.root, LINT_JSON)),
        _is_valid_security_json(Path(PROJECT_CONFIG.root, SECURITY_JSON)),
        _is_valid_coverage(Path(PROJECT_CONFIG.root, COVERAGE_DB)),
    ]
    if not all(all_is_valid_checks):
        sys.exit(1)


def _handle_validation_error(file: Path, message: str) -> bool:
    print(f"error in [{file.name}]: {message}", file=sys.stderr)
    return False


def _is_valid_lint_txt(file: Path) -> bool:
    content = file.read_text()
    expr = re.compile(r"^Your code has been rated at (\d+.\d+)/.*", re.MULTILINE)
    matches = expr.search(content)
    if not matches:
        _handle_validation_error(file, "Could not find a rating")
        return False
    return True


def _is_valid_lint_json(file: Path) -> bool:
    try:
        content = file.read_text()
        issues = json.loads(content)
    except json.JSONDecodeError as ex:
        _handle_validation_error(file, f"Invalid json file, details: {ex}")
        return False

    for number, issue in enumerate(issues):
        actual = set(issue.keys())
        missing = LINT_JSON_ATTRIBUTES - actual
        if len(missing) > 0:
            _handle_validation_error(
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
        return _handle_validation_error(file, f"Invalid json file, details: {ex}")

    missing = SECURITY_JSON_ATTRIBUTES - actual
    if len(missing) > 0:
        return _handle_validation_error(
            file,
            f"Invalid format, the file is missing the following attributes {missing}",
        )
    return True


def _is_valid_coverage(path: Path) -> bool:
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
    except sqlite3.Error as ex:
        return _handle_validation_error(
            path, f"database connection not possible, details: {ex}"
        )
    try:
        actual_tables = set(
            cursor.execute("select name from sqlite_schema where type == 'table'")
        )
    except sqlite3.Error as ex:
        return _handle_validation_error(
            path, f"schema query not possible, details: {ex}"
        )
    actual = {f[0] for f in actual_tables if (f[0] in COVERAGE_TABLES)}
    missing = COVERAGE_TABLES - actual
    if len(missing) > 0:
        return _handle_validation_error(
            path,
            f"Invalid database, the database is missing the following tables {missing}",
        )
    return True


@nox.session(name="artifacts:copy", python=False)
def copy_artifacts(session: Session) -> None:
    """
    Copy artifacts to the current directory
    """

    artifact_dir = Path(session.posargs[0])
    suffix = _python_version_suffix()
    _combine_coverage(session, artifact_dir, f"coverage{suffix}*/{COVERAGE_DB}")
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


def _prepare_coverage_xml(
    session: Session, source: Path, cwd: Optional[Path] = None
) -> None:
    """
    Prepare the coverage XML for input into Sonar

    The coverage XML is used within Sonar to determine the overall coverage in our
    project and the coverage associated with source code changes made in a PR. If the
    code coverage associated with changes made in our PR does not meet the set Sonar
    guidelines for that project, then when the sonarqubecloud bot writes in the PR, it
    will indicate that the coverage constraint was not met, &, if the bot is required in
    the branch protections for that project, then it will block the PR from being
    merged. Thus, in the preparation of the coverage XML, we set `--fail-under=0` so
    that this sub-step will not fail prior to sending the data to Sonar. Otherwise, this
    sub-step would fail whenever the `fail_under` in `[tool.coverage.report]` of the
    `pyproject.toml` was not met.
    """
    command = [
        "coverage",
        "xml",
        "-o",
        COVERAGE_XML,
        "--include",
        f"{source}/*",
        "--fail-under=0",
    ]
    output = subprocess.run(command, capture_output=True, text=True, cwd=cwd)  # nosec
    if output.returncode != 0:
        if output.stdout.strip() == "No data to report.":
            # Assuming that previous steps passed in the CI, this indicates — as
            # is in the case for newly created projects — that no coverage over the
            # `source` files was found. In this scenario, we do not need the CI to
            # break from a non-zero exit code. This is because without a coverage file
            # the sonarqubecloud bot will still report that the coverage is 0%, but as
            # long as the bot is not required in the project's branch protections, then
            # the PR can still be merged, provided that the other required constraints
            # have been met.
            return
        session.error(output.returncode, output.stdout, output.stderr)


def _upload_to_sonar(
    session: Session, sonar_token: Optional[str], config: Config
) -> None:
    command = [
        "pysonar",
        "--sonar-token",
        sonar_token,
        "--sonar-python-pylint-report-path",
        LINT_JSON,
        "--sonar-python-bandit-report-paths",
        SECURITY_JSON,
        "--sonar-python-version",
        ",".join(config.python_versions),
        "--sonar-sources",
        config.source,
    ]
    if Path(COVERAGE_XML).exists():
        command.extend(["--sonar-python-coverage-report-paths", COVERAGE_XML])
    session.run(*command)  # type: ignore


@nox.session(name="sonar:check", python=False)
def upload_artifacts_to_sonar(session: Session) -> None:
    """Upload artifacts to sonar for analysis"""
    sonar_token = os.getenv("SONAR_TOKEN")
    _prepare_coverage_xml(session, PROJECT_CONFIG.source)
    _upload_to_sonar(session, sonar_token, PROJECT_CONFIG)
