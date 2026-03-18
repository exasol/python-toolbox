from __future__ import annotations

import json
import re
import subprocess
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


class PoetryProject:
    def __init__(self, poetry_path: Path, path: Path):
        self.poetry = poetry_path
        self.dir = path

    @property
    def name(self) -> str:
        return self.dir.name

    @property
    def toml(self) -> Path:
        return self.dir / "pyproject.toml"

    def create(self) -> PoetryProject:
        aux_subprocess(self.poetry, "new", self.name, cwd=self.dir.parent)
        return self

    def set_minimum_python_version(self, version: str) -> PoetryProject:
        content = self.toml.read_text()
        changed = re.sub(
            r'^requires-python = ".*"$',
            f'requires-python = ">={version}"',
            content,
            flags=re.MULTILINE,
        )
        self.toml.write_text(changed)
        return self

    def add_package(self, spec: str) -> PoetryProject:
        aux_subprocess(self.poetry, "add", spec, cwd=self.dir)
        return self

    def add_to_toml(self, content: str) -> PoetryProject:
        with self.toml.open("a") as f:
            f.write(cleandoc(content))
        return self

    def install(self) -> PoetryProject:
        aux_subprocess(self.poetry, "install", cwd=self.dir)
        return self


@pytest.fixture
def create_poetry_project(tmp_path, sample_vulnerability, poetry_path, ptb_minimum_python_version):
    project = (
        PoetryProject(poetry_path, tmp_path / "vulnerability")
        .create()
        .set_minimum_python_version(ptb_minimum_python_version)
        .add_package(
            f"{sample_vulnerability.package_name}==" f"{sample_vulnerability.version}"
        )
        .add_to_toml("""
            [tool.poetry.requires-plugins]
            poetry-plugin-export = ">=1.8"
            """)
        .install()
    )
    return project.dir


def without_vuln_descriptions(dep: PipAuditEntry):
    def strip_description(entry: PipAuditEntry):
        return {k: v for k, v in entry.items() if k != "description"}

    def without_descriptions(vulnerabilities):
        return [strip_description(v) for v in vulnerabilities]

    return {k: (without_descriptions(v) if k == "vulns" else v) for k, v in dep.items()}


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
