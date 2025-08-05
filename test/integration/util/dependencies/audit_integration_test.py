import json
import subprocess
from inspect import cleandoc

import pytest

from exasol.toolbox.util.dependencies.audit import audit_poetry_files


@pytest.fixture
def create_poetry_project(tmp_path, sample_vulnerability, poetry_path):
    project_name = "vulnerability"
    subprocess.run([poetry_path, "new", project_name], cwd=tmp_path, env={})

    poetry_root_dir = tmp_path / project_name
    subprocess.run(
        [
            poetry_path,
            "add",
            f"{sample_vulnerability.package_name}=={sample_vulnerability.version}",
        ],
        cwd=poetry_root_dir,
        env={},
    )

    poetry_export = cleandoc(
        """
    [tool.poetry.requires-plugins]
    poetry-plugin-export = ">=1.8"
    """
    )

    with (poetry_root_dir / "pyproject.toml").open("a") as f:
        f.write(poetry_export)

    subprocess.run(
        [poetry_path, "install"],
        cwd=poetry_root_dir,
        env={},
    )

    return poetry_root_dir


class TestAuditPoetryFiles:
    @staticmethod
    def test_works_as_expected(create_poetry_project, sample_vulnerability):
        result = audit_poetry_files(working_directory=create_poetry_project)
        expected_innards = sample_vulnerability.pip_audit_vuln_entry.copy()
        expected_innards.pop("description")

        assert isinstance(result, str)
        result_dict = json.loads(result)

        for entry in result_dict["dependencies"]:
            if entry["name"] == sample_vulnerability.package_name:
                for vuln in entry["vulns"]:
                    vuln.pop("description")

                assert entry == {
                    "name": sample_vulnerability.package_name,
                    "version": sample_vulnerability.version,
                    "vulns": [expected_innards],
                }
