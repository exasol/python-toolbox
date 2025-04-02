import json
from inspect import cleandoc
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest

from exasol.toolbox.nox._dependencies import (
    Audit,
    DependencyUpdate,
    Package,
    PackageVersion,
    PackageVersionTracker,
    VulnerabilityTracker,
    _dependencies,
    _normalize,
    _packages_from_json,
    _packages_to_markdown,
)


@pytest.mark.parametrize(
    "toml,expected",
    [
        (
            """
[tool.poetry.dependencies]
pytest = ">=7.2.2,<9"
python = "^3.9"
            """,
            {"project": ["pytest", "python"]},
        ),
        (
            """
[tool.poetry.dependencies]
pytest = ">=7.2.2,<9"
python = "^3.9"

[tool.poetry.dev.dependencies]
pip-licenses = "^5.0.0"

[tool.poetry.group.dev.dependencies]
autoimport = "^1.4.0"
            """,
            {"project": ["pytest", "python"], "dev": ["pip-licenses", "autoimport"]},
        ),
    ],
)
def test_dependencies(toml, expected):
    actual = _dependencies(toml)
    assert actual == expected


@pytest.mark.parametrize(
    "licenses,expected",
    [
        ("The Unlicensed (Unlicensed); BSD License", "BSD"),
        ("BSD License; MIT License", "MIT"),
        ("MIT License; Mozilla Public License 2.0 (MPL 2.0)", "MPLv2"),
        (
            "Mozilla Public License 2.0 (MPL 2.0); GNU Lesser General Public License v2 (LGPLv2)",
            "LGPLv2",
        ),
        (
            "GNU Lesser General Public License v2 (LGPLv2); GNU General Public License v2 (GPLv2)",
            "GPLv2",
        ),
        (
            "GNU General Public License v2 (GPLv2); GNU General Public License v3 (GPLv3)",
            "GPLv3",
        ),
    ],
)
def test_normalize(licenses, expected):
    actual = _normalize(licenses)
    assert actual == expected


@pytest.mark.parametrize(
    "json,expected",
    [
        (
            """
[
    {
        "License": "license1",
        "Name": "name1",
        "URL": "link1",
        "Version": "version1"
    },
    {
        "License": "license2",
        "Name": "name2",
        "URL": "UNKNOWN",
        "Version": "version2"
    }
]
            """,
            [
                Package(
                    name="name1",
                    version="version1",
                    package_link="link1",
                    license="license1",
                    license_link="",
                ),
                Package(
                    name="name2",
                    version="version2",
                    package_link="",
                    license="license2",
                    license_link="",
                ),
            ],
        )
    ],
)
def test_packages_from_json(json, expected):
    actual = _packages_from_json(json)
    assert actual == expected


@pytest.mark.parametrize(
    "dependencies,packages,expected",
    [
        (
            {"project": ["package1", "package3"], "dev": ["package2"]},
            [
                Package(
                    name="package1",
                    package_link="package_link1",
                    version="version1",
                    license="license1",
                    license_link="license_link1",
                ),
                Package(
                    name="package2",
                    package_link="package_link2",
                    version="version2",
                    license="license2",
                    license_link="license_link2",
                ),
                Package(
                    name="package3",
                    package_link="package_link3",
                    version="version3",
                    license="license3",
                    license_link="",
                ),
            ],
            """# Dependencies
## Project Dependencies
|Package|version|Licence|
|---|---|---|
|[package1](package_link1)|version1|[license1](license_link1)|
|[package3](package_link3)|version3|license3|

## Dev Dependencies
|Package|version|Licence|
|---|---|---|
|[package2](package_link2)|version2|[license2](license_link2)|

""",
        )
    ],
)
def test_packages_to_markdown(dependencies, packages, expected):
    actual = _packages_to_markdown(dependencies, packages)
    assert actual == expected


@pytest.fixture
def audit_json_no_vulns():
    audit_dict = {
        "dependencies": [{"name": "alabaster", "version": "0.7.16", "vulns": []}]
    }
    return json.dumps(audit_dict).encode("utf-8")


class TestFilterJsonForVulnerabilities:

    @staticmethod
    def test_no_vulnerability_returns_empty_list(audit_json_no_vulns):
        expected = {"dependencies": []}

        actual = Audit._filter_json_for_vulnerabilities(audit_json_no_vulns)
        assert actual == expected

    @staticmethod
    def test_vulnerabilities_returned_in_list(pip_audit_report):
        audit_json = json.dumps(pip_audit_report).encode("utf-8")

        actual = Audit._filter_json_for_vulnerabilities(audit_json)
        assert actual == pip_audit_report


@pytest.fixture
def package_version_tracker():
    with patch.object(PackageVersionTracker, "__init__", return_value=None):
        pvm = PackageVersionTracker()
    return pvm


@pytest.fixture
def vulnerability_tracker():
    with patch.object(VulnerabilityTracker, "__init__", return_value=None):
        vm = VulnerabilityTracker()
    return vm


class TestPackageVersionTracker:
    @staticmethod
    @patch("subprocess.run")
    @pytest.mark.parametrize(
        "expected",
        [
            pytest.param(PackageVersion("bandit", "1.8.3"), id="3_digit_version"),
            pytest.param(PackageVersion("import-linter", "2.2"), id="2_digit_version"),
            pytest.param(PackageVersion("fake", "1"), id="1_digit_version"),
        ],
    )
    def test_obtain_version_tuple(
        mock_run, package_version_tracker, expected: PackageVersion
    ):
        mock_stdout = MagicMock()
        input_line = f"{expected.name}       {expected.version}     Dummy description."
        mock_stdout.configure_mock(stdout=input_line.encode("utf-8"))
        mock_run.return_value = mock_stdout

        actual = package_version_tracker._obtain_version_set()
        assert actual == {expected}

    @staticmethod
    @pytest.mark.parametrize(
        "before_env, after_env, expected",
        [
            pytest.param(
                {PackageVersion("bandit", "1.8.3")},
                {PackageVersion("bandit", "1.8.4")},
                "* Updated bandit (1.8.3 → 1.8.4)",
                id="updated_dependence_version",
            ),
            pytest.param(
                {},
                {PackageVersion("bandit", "1.8.4")},
                "* Added bandit (1.8.4)",
                id="added_dependence",
            ),
            pytest.param(
                {PackageVersion("bandit", "1.8.3")},
                {},
                "* Removed bandit (1.8.3)",
                id="removed_dependence",
            ),
        ],
    )
    def test_changes(
        package_version_tracker, before_env: set, after_env: set, expected: str
    ):
        package_version_tracker.before_env = before_env
        package_version_tracker.after_env = after_env
        actual = package_version_tracker.changes
        assert actual == (expected,)

    @staticmethod
    def test_packages(package_version_tracker):
        package_name = "bandit"
        package_version_tracker.before_env = {PackageVersion(package_name, "1.8.3")}

        actual = package_version_tracker.packages
        assert actual == {"bandit"}


class TestVulnerabilityTracker:
    @staticmethod
    def test_set_to_resolve_without_argument():
        mock_session = MagicMock()
        mock_session.posargs = []

        args = DependencyUpdate._parse_args(mock_session)
        actual = VulnerabilityTracker._set_to_resolve(args.vulnerability_issues)

        assert actual == set()

    @staticmethod
    def test_set_to_resolve_with_argument(
        tmp_path,
        pip_audit_cryptography_github_issue,
    ):
        file_path = tmp_path / "test.json"
        file_path.write_text(
            pip_audit_cryptography_github_issue.json_str, encoding="utf-8"
        )
        mock_session = MagicMock()
        mock_session.posargs = ["--vulnerability-issues", str(file_path)]

        args = DependencyUpdate._parse_args(mock_session)
        actual = VulnerabilityTracker._set_to_resolve(args.vulnerability_issues)

        assert actual == {pip_audit_cryptography_github_issue}

    @staticmethod
    @patch("subprocess.run")
    def test_split_resolution_status_audit_json_no_vulns(
        mock_run,
        audit_json_no_vulns,
        vulnerability_tracker,
        pip_audit_cryptography_github_issue,
    ):
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(stdout=audit_json_no_vulns)
        mock_run.return_value = mock_stdout

        vulnerability_tracker.to_resolve = {pip_audit_cryptography_github_issue}
        vulnerability_tracker._split_resolution_status()

        assert vulnerability_tracker.resolved == {pip_audit_cryptography_github_issue}
        assert vulnerability_tracker.not_resolved == set()

    @staticmethod
    @patch("subprocess.run")
    def test_split_resolution_status_audit_json_has_vulns(
        mock_run,
        vulnerability_tracker,
        pip_audit_report,
        pip_audit_cryptography_github_issue,
    ):
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(stdout=json.dumps(pip_audit_report).encode("utf-8"))
        mock_run.return_value = mock_stdout

        vulnerability_tracker.to_resolve = {pip_audit_cryptography_github_issue}
        vulnerability_tracker._split_resolution_status()

        assert vulnerability_tracker.resolved == set()
        assert vulnerability_tracker.not_resolved == {
            pip_audit_cryptography_github_issue
        }

    @staticmethod
    def test_get_packages(vulnerability_tracker, pip_audit_cryptography_github_issue):
        vulnerability_tracker.to_resolve = {pip_audit_cryptography_github_issue}
        dependency = pip_audit_cryptography_github_issue.coordinates.split(":")[0]

        actual = vulnerability_tracker.get_packages()
        assert actual == {dependency}

    @staticmethod
    def test_issues_not_resolved(
        vulnerability_tracker, pip_audit_cryptography_github_issue
    ):
        vulnerability_tracker.not_resolved = {pip_audit_cryptography_github_issue}

        actual = vulnerability_tracker.issues_not_resolved
        assert actual == (
            "* Did NOT resolve https://github.com/exasol/<repo-name>/issues/394 (CVE-2024-12797)",
        )

    @staticmethod
    def test_issues_resolved(
        vulnerability_tracker, pip_audit_cryptography_github_issue
    ):
        vulnerability_tracker.resolved = {pip_audit_cryptography_github_issue}

        actual = vulnerability_tracker.issues_resolved
        assert actual == (
            "* Closes https://github.com/exasol/<repo-name>/issues/394 (CVE-2024-12797)",
        )

    @staticmethod
    def test_summary(vulnerability_tracker, pip_audit_cryptography_github_issue):
        vulnerability_tracker.resolved = {pip_audit_cryptography_github_issue}

        actual = vulnerability_tracker.summary
        assert actual == (
            cleandoc(
                """CVE-2024-12797 in dependency `cryptography:43.0.3`
 pyca / cryptography's wheels include a statically linked copy of 
OpenSSL. The versions of OpenSSL included in  cryptography 42.0.0 - 44.0.0 
are vulnerable to a security issue. More details about the vulnerability 
itself can be found in https://openssl-library.org/news/secadv/20250211.txt. 
If you are building cryptography source("sdist") then you are responsible 
for upgrading your copy of OpenSSL. Only users installing from wheels built 
by the cryptography project(i.e., those distributed on PyPI) need to update 
their cryptography versions.
            """
            ),
        )

    @staticmethod
    def test_vulnerabilities_resolved(
        vulnerability_tracker, pip_audit_cryptography_github_issue
    ):
        vulnerability_tracker.resolved = {pip_audit_cryptography_github_issue}

        actual = vulnerability_tracker.vulnerabilities_resolved
        assert actual == (
            "* #394 Fixed vulnerability CVE-2024-12797 in `cryptography:43.0.3`",
        )
