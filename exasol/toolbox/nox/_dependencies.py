from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.util.dependencies.licenses import (
    PackageLicenseReport,
    get_licenses,
)
from exasol.toolbox.util.dependencies.poetry_dependencies import get_dependencies


class Audit:
    @staticmethod
    def _filter_json_for_vulnerabilities(audit_json_bytes: bytes) -> dict:
        """
        Filters JSON from pip-audit for only packages with vulnerabilities

        Examples:
        >>> audit_json_dict = {"dependencies": [
        ... {"name": "alabaster", "version": "0.7.16", "vulns": []},
        ... {"name": "cryptography", "version": "43.0.3", "vulns":
        ... [{"id": "GHSA-79v4-65xg-pq4g", "fix_versions": ["44.0.1"],
        ... "aliases": ["CVE-2024-12797"],
        ... "description": "pyca/cryptography\'s wheels..."}]}]}
        >>> audit_json = json.dumps(audit_json_dict).encode()
        >>> Audit._filter_json_for_vulnerabilities(audit_json)
        {"dependencies": [{"name": "cryptography", "version": "43.0.3", "vulns":
        [{"id": "GHSA-79v4-65xg-pq4g", "fix_versions": ["44.0.1"], "aliases":
        ["CVE-2024-12797"], "description": "pyca/cryptography\'s wheels..."}]}]}
        """
        audit_dict = json.loads(audit_json_bytes.decode("utf-8"))
        return {
            "dependencies": [
                {
                    "name": entry["name"],
                    "version": entry["version"],
                    "vulns": entry["vulns"],
                }
                for entry in audit_dict["dependencies"]
                if entry["vulns"]
            ]
        }

    @staticmethod
    def _parse_args(session) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Audits dependencies for security vulnerabilities",
            usage="nox -s dependency:audit -- -- [options]",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=Path,
            default=None,
            help="Output results to the given file",
        )
        return parser.parse_args(args=session.posargs)

    def run(self, session: Session) -> None:
        args = self._parse_args(session)

        command = ["pip-audit", "-f", "json"]
        output = subprocess.run(command, capture_output=True)

        audit_json = self._filter_json_for_vulnerabilities(output.stdout)
        if args.output:
            with open(args.output, "w") as file:
                json.dump(audit_json, file)
        else:
            print(json.dumps(audit_json, indent=2))

        if output.returncode != 0:
            session.warn(
                f"Command {' '.join(command)} failed with exit code {output.returncode}",
            )


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
    Audit().run(session=session)
