from __future__ import annotations

import json
import subprocess  # nosec
import tempfile
from dataclasses import dataclass
from pathlib import Path
from re import search
from typing import (
    Any,
    Union,
)

from pydantic import BaseModel

from exasol.toolbox.util.dependencies.shared_models import Package

PIP_AUDIT_VULNERABILITY_PATTERN = (
    r"^Found \d+ known vulnerabilit\w{1,3} in \d+ package\w?$"
)


@dataclass
class PipAuditException(Exception):
    return_code: int
    stdout: str
    stderr: str

    def __init__(self, subprocess_output: subprocess.CompletedProcess) -> None:
        self.return_code = subprocess_output.returncode
        self.stdout = subprocess_output.stdout
        self.stderr = subprocess_output.stderr


class Vulnerability(Package):
    id: str
    aliases: list[str]
    fix_versions: list[str]
    description: str

    @classmethod
    def from_audit_entry(
        cls, package_name: str, version: str, vuln_entry: dict[str, Any]
    ) -> Vulnerability:
        """
        Create a Vulnerability from a pip-audit vulnerability entry
        """
        return cls(
            name=package_name,
            version=version,
            id=vuln_entry["id"],
            aliases=vuln_entry["aliases"],
            fix_versions=vuln_entry["fix_versions"],
            description=vuln_entry["description"],
        )

    @property
    def security_issue_entry(self) -> dict[str, Union[str, list[str]]]:
        return {
            "name": self.name,
            "version": str(self.version),
            "refs": [self.id] + self.aliases,
            "description": self.description,
        }


def audit_poetry_files(working_directory: Path) -> str:
    """
    Audit the `pyproject.toml` and `poetry.lock` files

    pip-audit evaluates installed packages. This is to provide
    additional security-related information beyond seeing if a given package
    has a known vulnerability. Thus, to audit our `pyproject.toml` and
    `poetry.lock` files without altering a locally sourced poetry environment,
    this function first exports the locked packages to a requirements.txt file.
    Then, pip-audit evaluates the requirements.txt by installing them to a virtualenv
    and then inspecting the dependencies.
    """

    requirements_txt = "requirements.txt"
    output = subprocess.run(
        ["poetry", "export", "--format=requirements.txt"],
        capture_output=True,
        text=True,
        cwd=working_directory,
    )  # nosec
    if output.returncode != 0:
        raise PipAuditException(subprocess_output=output)

    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        (tmpdir / requirements_txt).write_text(output.stdout)

        command = ["pip-audit", "-r", requirements_txt, "-f", "json"]
        output = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )  # nosec

    if output.returncode != 0:
        # pip-audit does not distinguish between 1) finding vulnerabilities
        # and 2) other errors performing the pip-audit (i.e. malformed file);
        # they both map to returncode = 1, so we have our own logic to raise errors
        # for the case of 2) and not 1).
        if not search(PIP_AUDIT_VULNERABILITY_PATTERN, output.stderr.strip()):
            raise PipAuditException(subprocess_output=output)
    return output.stdout


class Vulnerabilities(BaseModel):
    vulnerabilities: list[Vulnerability]

    @classmethod
    def load_from_pip_audit(cls, working_directory: Path) -> Vulnerabilities:
        """
        Convert the pip-audit JSON output into a Vulnerabilities model

        The output from pip-audit is a JSON, which as a dictionary looks like:
        >>> audit_dict = {"dependencies": [
        ... {"name": "alabaster", "version": "0.7.16", "vulns": []},
        ... {"name": "cryptography", "version": "43.0.3", "vulns":
        ... [{"id": "GHSA-79v4-65xg-pq4g", "fix_versions": ["44.0.1"],
        ... "aliases": ["CVE-2024-12797"],
        ... "description": "pyca/cryptography\'s wheels..."}, ...]}]}
        """
        audit_json = audit_poetry_files(working_directory)
        audit_dict = json.loads(audit_json)

        vulnerabilities = []
        for entry in audit_dict["dependencies"]:
            for vuln_entry in entry["vulns"]:
                vulnerabilities.append(
                    Vulnerability.from_audit_entry(
                        package_name=entry["name"],
                        version=entry["version"],
                        vuln_entry=vuln_entry,
                    )
                )
        return Vulnerabilities(vulnerabilities=vulnerabilities)

    @property
    def security_issue_dict(self) -> list[dict[str, Union[str, list[str]]]]:
        return [
            vulnerability.security_issue_entry for vulnerability in self.vulnerabilities
        ]
