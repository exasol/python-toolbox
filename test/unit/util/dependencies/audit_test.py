import json
from pathlib import Path
from subprocess import CompletedProcess
from unittest import mock
from unittest.mock import MagicMock

import pytest

from exasol.toolbox.util.dependencies.audit import (
    PipAuditException,
    Vulnerabilities,
    Vulnerability,
    VulnerabilitySource,
    audit_poetry_files,
    get_vulnerabilities,
    get_vulnerabilities_from_latest_tag,
)
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def mock_poetry_export():
    result = MagicMock(CompletedProcess)
    result.returncode = 0
    result.stdout = "dummy_requirements_content"
    result.stderr = ""
    return result


class TestVulnerability:
    @staticmethod
    def test_from_audit_entry(sample_vulnerability):
        result = sample_vulnerability.vulnerability
        assert result == Vulnerability(
            name=sample_vulnerability.package_name,
            version=sample_vulnerability.version,
            id=sample_vulnerability.vulnerability_id,
            aliases=[sample_vulnerability.cve_id],
            fix_versions=[sample_vulnerability.fix_version],
            description=sample_vulnerability.description,
        )

    @staticmethod
    def test_security_issue_entry(sample_vulnerability):
        assert (
            sample_vulnerability.vulnerability.security_issue_entry
            == sample_vulnerability.security_issue_entry
        )


class TestAuditPoetryFiles:
    @staticmethod
    @mock.patch("subprocess.run")
    def test_poetry_export_fails(mock_run):
        result = MagicMock(CompletedProcess)
        result.returncode = 1
        result.stdout = ""
        result.stderr = "pyproject.toml changed significantly since poetry.lock was last generated. Run `poetry lock` to fix the lock file.\n"
        mock_run.return_value = result

        with pytest.raises(PipAuditException) as e:
            audit_poetry_files(working_directory=Path())
        assert e.value.stderr == result.stderr

    @staticmethod
    @mock.patch("subprocess.run")
    def test_found_vulnerability_passes(
        mock_run, mock_poetry_export, sample_vulnerability
    ):
        mock_pip_audit = MagicMock(CompletedProcess)
        mock_pip_audit.returncode = 1
        mock_pip_audit.stdout = sample_vulnerability.pip_audit_json
        mock_pip_audit.stderr = "Found 1 known vulnerability in 1 package"

        mock_run.side_effect = [
            mock_poetry_export,  # poetry export passes
            mock_pip_audit,  # pip-audit finds vulnerability
        ]

        result = audit_poetry_files(working_directory=Path())
        assert result == mock_pip_audit.stdout

    @staticmethod
    @mock.patch("subprocess.run")
    def test_pip_audit_failed_due_to_another_issue(mock_run, mock_poetry_export):
        mock_pip_audit = MagicMock(CompletedProcess)
        mock_pip_audit.returncode = 1
        mock_pip_audit.stdout = ""
        mock_pip_audit.stderr = (
            "ERROR:pip_audit._cli:Failed to upgrade `pip`:"
            " ['/tmp/tmpjcn9gz0d/bin/python', '-m', 'pip', 'install',"
            " '--upgrade', 'pip', 'wheel', 'setuptools']"
        )

        mock_run.side_effect = [
            mock_poetry_export,  # poetry export passes
            mock_pip_audit,  # pip-audit failed
        ]

        with pytest.raises(PipAuditException) as e:
            audit_poetry_files(working_directory=Path())
        assert e.value.stderr == mock_pip_audit.stderr


class TestVulnerabilities:
    @staticmethod
    def test_with_no_vulnerabilities():
        pip_audit_dict = {
            "dependencies": [{"name": "alabaster", "version": "0.7.16", "vulns": []}]
        }
        pip_audit_json = json.dumps(pip_audit_dict)

        with mock.patch(
            "exasol.toolbox.util.dependencies.audit.audit_poetry_files",
            return_value=pip_audit_json,
        ):
            result = Vulnerabilities.load_from_pip_audit(working_directory=Path())

        assert result == Vulnerabilities(vulnerabilities=[])

    @staticmethod
    def test_with_vulnerability(sample_vulnerability):
        with mock.patch(
            "exasol.toolbox.util.dependencies.audit.audit_poetry_files",
            return_value=sample_vulnerability.pip_audit_json,
        ):
            result = Vulnerabilities.load_from_pip_audit(working_directory=Path())

        assert result == Vulnerabilities(
            vulnerabilities=[sample_vulnerability.vulnerability]
        )

    @staticmethod
    def test_security_issue_dict(sample_vulnerability):
        vulnerabilities = Vulnerabilities(
            vulnerabilities=[sample_vulnerability.vulnerability]
        )
        result = vulnerabilities.security_issue_dict
        assert result == [sample_vulnerability.security_issue_entry]


@pytest.mark.parametrize(
    "prefix,expected",
    [
        pytest.param("DUMMY", None, id="without_a_matching_prefix_returns_none"),
        pytest.param(
            f"{VulnerabilitySource.CWE.value.lower()}-1234",
            VulnerabilitySource.CWE,
            id="with_matching_prefix_returns_vulnerability_source",
        ),
    ],
)
def test_from_prefix(prefix: str, expected):
    assert VulnerabilitySource.from_prefix(prefix) == expected


class TestGetVulnerabilities:
    def test_with_mock(self, sample_vulnerability):
        with mock.patch(
            "exasol.toolbox.util.dependencies.audit.audit_poetry_files",
            return_value=sample_vulnerability.pip_audit_json,
        ):
            result = get_vulnerabilities(PROJECT_CONFIG.root)

        # if successful, no errors & should be 1 due to mock
        assert isinstance(result, list)
        assert len(result) == 1


class TestGetVulnerabilitiesFromLatestTag:
    def test_with_mock(self, sample_vulnerability):
        with mock.patch(
            "exasol.toolbox.util.dependencies.audit.audit_poetry_files",
            return_value=sample_vulnerability.pip_audit_json,
        ):
            result = get_vulnerabilities_from_latest_tag()

        # if successful, no errors & should be 1 due to mock
        assert isinstance(result, list)
        assert len(result) == 1
