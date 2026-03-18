import json
import re
import subprocess
import sys
from inspect import cleandoc
from pathlib import Path

import pytest

from exasol.toolbox.util.dependencies.audit import (
    PipAuditEntry,
    audit_poetry_files,
)


def aux_subprocess(*cmd, **kwargs) -> subprocess.CompletedProcess:
    """
    Runs the specified command via subprocess with default kwargs suitable
    for running auxiliary commands, e.g. in pytest fixtures.

    The command is an executable incl its args and CLI options.

    The default kwargs are

    * Raise an exception on non-zero returncode
    * Capture output to keep pytest output clean
    * Use empty environment (no env variables)
    """
    kwargs_with_defaults = {
        "env": {},
        "check": True,
        "capture_output": True,
    } | kwargs
    return subprocess.run(cmd, **kwargs_with_defaults)


def set_minimum_python_version(file: Path, version):
    content = file.read_text()
    changed = re.sub(
        r'^requires-python = ".*"$',
        f'requires-python = ">={version.major}.{version.minor}"',
        content,
        flags=re.MULTILINE,
    )
    file.write_text(changed)


@pytest.fixture
def create_poetry_project(tmp_path, sample_vulnerability, poetry_path):
    project_name = "vulnerability"
    aux_subprocess(poetry_path, "new", project_name, cwd=tmp_path)

    poetry_root_dir = tmp_path / project_name
    set_minimum_python_version(poetry_root_dir / "pyproject.toml", sys.version_info)
    aux_subprocess(
        poetry_path,
        "add",
        f"{sample_vulnerability.package_name}=={sample_vulnerability.version}",
        cwd=poetry_root_dir,
    )

    poetry_export = cleandoc(
        """
        [tool.poetry.requires-plugins]
        poetry-plugin-export = ">=1.8"
        """
    )
    with (poetry_root_dir / "pyproject.toml").open("a") as f:
        f.write(poetry_export)

    aux_subprocess(poetry_path, "install", cwd=poetry_root_dir)
    return poetry_root_dir


def without_vuln_descriptions(dep: PipAuditEntry):
    def strip_description(entry: PipAuditEntry):
        return {k: v for k, v in entry.items() if k != "description"}

    def without_descriptions(vulnerabilities):
        return [strip_description(v) for v in vulnerabilities]

    return {
        k: (without_descriptions(v) if k == "vulns" else v)
        for k, v in dep.items()
    }


def find_dependency(dependencies: list[PipAuditEntry], name: str) -> PipAuditEntry:
    generator = (d for d in dependencies if d["name"] == name)
    return next(generator)


def test_pip_audit(create_poetry_project, sample_vulnerability):
    vuln = sample_vulnerability
    audit_output = audit_poetry_files(working_directory=create_poetry_project)
    result = json.loads(audit_output)
    actual = find_dependency(result["dependencies"], vuln.package_name)

    expected = {
        "name": vuln.package_name,
        "version": vuln.version,
        "vulns": [vuln.pip_audit_vuln_entry],
    }
    assert without_vuln_descriptions(actual) == without_vuln_descriptions(expected)
