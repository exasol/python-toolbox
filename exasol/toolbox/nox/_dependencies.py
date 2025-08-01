from __future__ import annotations

import json
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.util.dependencies.audit import (
    PipAuditException,
    Vulnerabilities,
)
from exasol.toolbox.util.dependencies.licenses import (
    PackageLicenseReport,
    get_licenses,
)
from exasol.toolbox.util.dependencies.poetry_dependencies import get_dependencies


@nox.session(name="dependency:licenses", python=False)
def dependency_licenses(session: Session) -> None:
    """Return the packages with their licenses"""
    dependencies = get_dependencies(working_directory=Path())
    licenses = get_licenses()
    license_markdown = PackageLicenseReport(
        dependencies=dependencies, licenses=licenses
    )
    print(license_markdown.to_markdown())


@nox.session(name="dependency:audit", python=False)
def audit(session: Session) -> None:
    """Check for known vulnerabilities"""

    try:
        vulnerabilities = Vulnerabilities.load_from_pip_audit(working_directory=Path())
    except PipAuditException as e:
        session.error(e.return_code, e.stdout, e.stderr)

    security_issue_dict = vulnerabilities.security_issue_dict
    print(json.dumps(security_issue_dict, indent=2))
