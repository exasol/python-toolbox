from __future__ import annotations

import argparse
import json
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import validate_path_within_root
from exasol.toolbox.util.dependencies.audit import (
    PipAuditException,
    Vulnerabilities,
    get_vulnerabilities,
    get_vulnerabilities_from_latest_tag,
)
from exasol.toolbox.util.dependencies.licenses import (
    PackageLicenseReport,
    get_licenses,
)
from exasol.toolbox.util.dependencies.poetry_dependencies import get_dependencies
from exasol.toolbox.util.dependencies.track_vulnerabilities import DependenciesAudit
from exasol.toolbox.util.dependencies.update_dependencies import DependencyUpdater
from noxconfig import PROJECT_CONFIG


def _format_update_vulnerabilities_message(was_updated: bool, report_json: str) -> str:
    if not was_updated:
        return "No vulnerable dependencies were found."
    if report_json == "[]":
        return "No vulnerable dependencies remain after updating."
    return report_json


@nox.session(name="dependency:licenses", python=False)
def dependency_licenses(session: Session) -> None:
    """Report licenses for all dependencies."""
    dependencies = get_dependencies(working_directory=Path())
    licenses = get_licenses()
    license_markdown = PackageLicenseReport(
        dependencies=dependencies, licenses=licenses
    )
    print(license_markdown.to_markdown())


@nox.session(name="dependency:audit", python=False)
def audit(session: Session) -> None:
    """Report known vulnerabilities."""
    try:
        vulnerabilities = Vulnerabilities.load_from_pip_audit(
            working_directory=PROJECT_CONFIG.root_path
        )
    except PipAuditException as e:
        session.error(e.returncode, e.stdout, e.stderr)

    security_issue_dict = vulnerabilities.security_issue_dict
    print(json.dumps(security_issue_dict, indent=2))


@nox.session(name="vulnerabilities:update", python=False)
def update_vulnerabilities(session: Session) -> None:
    """
    Update vulnerabilities and optionally save the JSON of remaining vulnerabilities
    to a file provided on the command line.
    """
    parser = argparse.ArgumentParser(
        prog="nox -s vulnerabilities:update",
        description="Update vulnerable dependencies and optionally write a report file.",
    )
    parser.add_argument(
        "report_filename",
        nargs="?",
        help="Optional filename for the JSON report of remaining vulnerabilities.",
    )
    args = parser.parse_args(session.posargs)

    try:
        dependency_updater = DependencyUpdater(root_path=PROJECT_CONFIG.root_path)
        was_updated, report_json = dependency_updater.update_vulnerable_dependencies()
    except PipAuditException as e:
        session.error(e.returncode, e.stdout, e.stderr)

    if args.report_filename is None:
        print(_format_update_vulnerabilities_message(was_updated, report_json))
        return

    report_path = validate_path_within_root(
        PROJECT_CONFIG.root_path / args.report_filename
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_json + "\n", encoding="utf-8")


@nox.session(name="vulnerabilities:resolved", python=False)
def report_resolved_vulnerabilities(session: Session) -> None:
    """Report resolved vulnerabilities in dependencies."""
    path = PROJECT_CONFIG.root_path
    audit = DependenciesAudit(
        previous_vulnerabilities=get_vulnerabilities_from_latest_tag(path),
        current_vulnerabilities=get_vulnerabilities(path),
    )
    print(audit.report_resolved_vulnerabilities())


@nox.session(name="dependency:sbom", python=False)
def generate_sbom(session: Session) -> None:
    """Generate SPDX SBOM for the project dependencies.

    Note: SPDX version 2 is used as no stable Python tool exists yet
    for generating SPDX version 3.
    """
    bom_cdx_json = PROJECT_CONFIG.root_path / "bom.cdx.json"
    bom_spdx_json = PROJECT_CONFIG.root_path / "bom.spdx.json"
    session.run("cyclonedx-py", "environment", "-o", bom_cdx_json)
    session.run(
        "sbomconvert",
        "-i",
        bom_cdx_json,
        "--sbom",
        "spdx",
        "--format",
        "json",
        "-o",
        bom_spdx_json,
    )
    session.run("test", "-s", bom_spdx_json)
