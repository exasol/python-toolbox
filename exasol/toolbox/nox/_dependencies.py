from __future__ import annotations

import json
from pathlib import Path

import nox
from nox import Session

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
from noxconfig import PROJECT_CONFIG


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
        vulnerabilities = Vulnerabilities.load_from_pip_audit(working_directory=Path())
    except PipAuditException as e:
        session.error(e.returncode, e.stdout, e.stderr)

    security_issue_dict = vulnerabilities.security_issue_dict
    print(json.dumps(security_issue_dict, indent=2))


@nox.session(name="vulnerabilities:resolved", python=False)
def report_resolved_vulnerabilities(session: Session) -> None:
    """Report resolved vulnerabilities in dependencies."""
    path = PROJECT_CONFIG.root_path
    audit = DependenciesAudit(
        previous_vulnerabilities=get_vulnerabilities_from_latest_tag(path),
        current_vulnerabilities=get_vulnerabilities(path),
    )
    print(audit.report_resolved_vulnerabilities())
