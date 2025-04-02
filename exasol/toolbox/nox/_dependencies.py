from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from contextlib import contextmanager
from dataclasses import (
    dataclass,
    field,
)
from inspect import cleandoc
from json import loads
from pathlib import Path
from subprocess import CompletedProcess

import nox
import tomlkit
from nox import Session

from exasol.toolbox.security import (
    GitHubVulnerabilityIssue,
    from_pip_audit,
)


@dataclass(frozen=True)
class Package:
    name: str
    package_link: str
    version: str
    license: str
    license_link: str


def _dependencies(toml_str: str) -> dict[str, list]:
    toml = tomlkit.loads(toml_str)
    poetry = toml.get("tool", {}).get("poetry", {})
    dependencies: dict[str, list] = {}

    packages = poetry.get("dependencies", {})
    if packages:
        dependencies["project"] = [package for package in packages]

    packages = poetry.get("dev", {}).get("dependencies", {})
    if packages:
        dependencies["dev"] = [package for package in packages]

    groups = poetry.get("group", {})
    for group in groups:
        packages = groups.get(group, {}).get("dependencies")
        if packages and not dependencies.get(group, {}):
            dependencies[group] = []
        for package in packages:
            dependencies[group].append(package)
    return dependencies


def _normalize(_license: str) -> str:
    def is_multi_license(l):
        return ";" in l

    def select_most_restrictive(licenses: list) -> str:
        _max = 0
        lic = "Unknown"
        _mapping = {
            "Unknown": -1,
            "Unlicensed": 0,
            "BSD": 1,
            "MIT": 2,
            "MPLv2": 3,
            "LGPLv2": 4,
            "GPLv2": 5,
            "GPLv3": 6,
        }
        for l in licenses:
            if l in _mapping:
                if _mapping[l] > _mapping[lic]:
                    lic = l
            else:
                return "<br>".join(licenses)
        return lic

    mapping = {
        "BSD License": "BSD",
        "MIT License": "MIT",
        "The Unlicensed (Unlicensed)": "Unlicensed",
        "Mozilla Public License 2.0 (MPL 2.0)": "MPLv2",
        "GNU General Public License (GPL)": "GPL",
        "GNU Lesser General Public License v2 (LGPLv2)": "LGPLv2",
        "GNU General Public License v2 (GPLv2)": "GPLv2",
        "GNU General Public License v2 or later (GPLv2+)": "GPLv2+",
        "GNU General Public License v3 (GPLv3)": "GPLv3",
        "Apache Software License": "Apache",
    }

    if is_multi_license(_license):
        items = []
        for item in _license.split(";"):
            item = str(item).strip()
            if item in mapping:
                items.append(mapping[item])
            else:
                items.append(item)
        return select_most_restrictive(items)

    if _license not in mapping:
        return _license

    return mapping[_license]


def _packages_from_json(json: str) -> list[Package]:
    packages = loads(json)
    packages_list = []
    mapping = {
        "GPLv1": "https://www.gnu.org/licenses/old-licenses/gpl-1.0.html",
        "GPLv2": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
        "LGPLv2": "https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html",
        "GPLv3": "https://www.gnu.org/licenses/gpl-3.0.html",
        "LGPLv3": "https://www.gnu.org/licenses/lgpl-3.0.html",
        "Apache": "https://www.apache.org/licenses/LICENSE-2.0",
        "MIT": "https://mit-license.org/",
        "BSD": "https://opensource.org/license/bsd-3-clause",
    }
    for package in packages:
        package_license = _normalize(package["License"])
        packages_list.append(
            Package(
                name=package["Name"],
                package_link="" if package["URL"] == "UNKNOWN" else package["URL"],
                version=package["Version"],
                license=package_license,
                license_link=(
                    "" if package_license not in mapping else mapping[package_license]
                ),
            )
        )
    return packages_list


def _licenses() -> list[Package]:
    with tempfile.NamedTemporaryFile() as file:
        subprocess.run(
            [
                "poetry",
                "run",
                "pip-licenses",
                "--format=json",
                "--output-file=" + file.name,
                "--with-system",
                "--with-urls",
            ],
            capture_output=True,
        )
        result = _packages_from_json(file.read().decode())
    return result


def _packages_to_markdown(
    dependencies: dict[str, list], packages: list[Package]
) -> str:
    def heading():
        text = "# Dependencies\n"
        return text

    def dependency(group: str, group_packages: list, packages: list[Package]) -> str:
        def _header(_group: str):
            _group = "".join([word.capitalize() for word in _group.strip().split()])
            text = f"## {_group} Dependencies\n"
            text += "|Package|version|Licence|\n"
            text += "|---|---|---|\n"
            return text

        def _rows(_group_packages: list, _packages: list[Package]) -> str:
            def _normalize_package_name(name: str) -> str:
                _name = name.lower()
                while "_" in _name:
                    _name = _name.replace("_", "-")
                return _name

            text = ""
            for package in _group_packages:
                consistent = filter(
                    lambda elem: (_normalize_package_name(elem.name) == package),
                    _packages,
                )
                for content in consistent:
                    if content.package_link:
                        text += f"|[{content.name}]({content.package_link})"
                    else:
                        text += f"|{content.name}"
                    text += f"|{content.version}"
                    if content.license_link:
                        text += f"|[{content.license}]({content.license_link})|\n"
                    else:
                        text += f"|{content.license}|\n"
            text += "\n"
            return text

        _template = cleandoc(
            """
            {header}{rows}
        """
        )
        return _template.format(
            header=_header(group), rows=_rows(group_packages, packages)
        )

    template = cleandoc(
        """
        {heading}{rows}
    """
    )

    rows = ""
    for group in dependencies:
        rows += dependency(group, dependencies[group], packages)
    return template.format(heading=heading(), rows=rows)


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

    def audit(self) -> tuple[dict, CompletedProcess]:
        command = ("poetry", "run", "pip-audit", "-f", "json")
        output = subprocess.run(command, capture_output=True)
        audit_json = self._filter_json_for_vulnerabilities(output.stdout)
        return audit_json, output

    def run(self, session: Session) -> None:
        args = self._parse_args(session)
        audit_json, output = self.audit()
        if args.output:
            with open(args.output, "w") as file:
                json.dump(audit_json, file)
        else:
            print(json.dumps(audit_json, indent=2))

        if output.returncode != 0:
            session.warn(
                f"Command {' '.join(output.args)} failed with exit code {output.returncode}",
            )


@dataclass(frozen=True)
class PackageVersion:
    name: str
    version: str


@dataclass
class PackageVersionTracker:
    """
    Tracks direct dependencies for package versions before & after updates

    Assumption:
      - The dependency ranges in the pyproject.toml allows users to often update
      transitive dependencies on their own. It is, therefore, more important for us to
      track the changes of direct dependencies and, if present, the resolution of both
      vulnerabilities for direct and transitive dependencies.
    """

    before_env: set[PackageVersion] = field(default_factory=set)
    after_env: set[PackageVersion] = field(default_factory=set)

    @staticmethod
    def _obtain_version_set() -> set[PackageVersion]:
        def _get_package_version(line: str) -> PackageVersion:
            pattern = r"\s+(\d+(?:\.\d+)*)\s+"
            groups = re.split(pattern, line)
            return PackageVersion(name=groups[0], version=groups[1])

        command = ("poetry", "show", "--top-level")
        result = subprocess.run(command, capture_output=True, check=True)
        return {
            _get_package_version(line)
            for line in result.stdout.decode("utf-8").splitlines()
        }

    @property
    def changes(self) -> tuple:
        before_update_dict = {pkg.name: pkg for pkg in self.before_env}
        after_update_dict = {pkg.name: pkg for pkg in self.after_env}

        def _get_change_str(pkg_name: str) -> str | None:
            if pkg_name not in after_update_dict.keys():
                entry = before_update_dict[pkg_name]
                return f"* Removed {entry.name} ({entry.version})"
            if pkg_name not in before_update_dict.keys():
                entry = after_update_dict[pkg_name]
                return f"* Added {entry.name} ({entry.version})"
            before_entry = before_update_dict[pkg_name]
            after_entry = after_update_dict[pkg_name]
            if before_entry.version != after_entry.version:
                return f"* Updated {pkg_name} ({before_entry.version} → {after_entry.version})"
            return None

        all_packages = before_update_dict.keys() | after_update_dict.keys()
        return tuple(
            change_str
            for pkg_name in all_packages
            if (change_str := _get_change_str(pkg_name))
        )

    @property
    def packages(self) -> set[str]:
        return {pkg.name for pkg in self.before_env}

    def __enter__(self) -> PackageVersionTracker:
        self.before_env = self._obtain_version_set()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.after_env = self._obtain_version_set()


@contextmanager
def managed_file(file_obj: argparse.FileType):
    """Context manager to manage a file provided by argparse"""
    yield file_obj


@dataclass
class VulnerabilityTracker:
    """Tracks the resolution of GitHubVulnerabilityIssues before & after updates"""

    to_resolve: set[GitHubVulnerabilityIssue] = field(default_factory=set)
    resolved: set[GitHubVulnerabilityIssue] = field(default_factory=set)
    not_resolved: set[GitHubVulnerabilityIssue] = field(default_factory=set)

    def __init__(self, vulnerability_issues: argparse.FileType | None):
        self.to_resolve: set[GitHubVulnerabilityIssue] = self._set_to_resolve(
            vulnerability_issues
        )

    @staticmethod
    def _set_to_resolve(
        vulnerability_issues: argparse.FileType | None,
    ) -> set[GitHubVulnerabilityIssue]:
        if not vulnerability_issues:
            return set()
        with managed_file(vulnerability_issues) as f:
            lines = f.readlines()
        return set(GitHubVulnerabilityIssue.extract_from_jsonl(lines))

    def _split_resolution_status(self) -> None:
        to_resolve_by_cve = {vuln.cve: vuln for vuln in self.to_resolve}
        cves_to_resolve = set(to_resolve_by_cve.keys())

        audit_json, _ = Audit().audit()
        cve_audit = {vuln.cve for vuln in from_pip_audit(json.dumps(audit_json))}

        cves_not_resolved = cves_to_resolve.intersection(cve_audit)

        self.not_resolved = {to_resolve_by_cve[cve] for cve in cves_not_resolved}
        self.resolved = self.to_resolve - self.not_resolved

    def get_packages(self) -> set[str]:
        return {vuln.coordinates.split(":")[0] for vuln in self.to_resolve}

    @property
    def issues_not_resolved(self) -> tuple[str, ...]:
        return tuple(
            f"* Did NOT resolve {vuln.issue_url} ({vuln.cve})"
            for vuln in self.not_resolved
        )

    @property
    def issues_resolved(self) -> tuple[str, ...]:
        return tuple(
            f"* Closes {vuln.issue_url} ({vuln.cve})" for vuln in self.resolved
        )

    @property
    def summary(self) -> tuple[str, ...]:
        return tuple(
            cleandoc(
                f"""{vuln.cve} in dependency `{vuln.coordinates}`\n {vuln.description}
            """
            )
            for vuln in self.resolved
        )

    @property
    def vulnerabilities_resolved(self) -> tuple[str, ...]:
        def get_issue_number(issue_url: str) -> str | None:
            pattern = r"/issues/(\d+)$"
            match = re.search(pattern, issue_url)
            return match.group(1) if match else None

        return tuple(
            f"* #{get_issue_number(vuln.issue_url)} Fixed vulnerability {vuln.cve} in `{vuln.coordinates}`"
            for vuln in self.resolved
        )

    def __enter__(self) -> VulnerabilityTracker:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._split_resolution_status()


@dataclass(frozen=True)
class DependencyChanges:
    package_changes: tuple[str, ...]
    issues_resolved: tuple[str, ...]
    issues_not_resolved: tuple[str, ...]
    vulnerabilities_resolved: tuple[str, ...]
    vulnerabilities_resolved_summary: tuple[str, ...]


class DependencyUpdate:
    """Update dependencies"""

    @staticmethod
    def _parse_args(session) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Updates dependencies & returns changes",
            usage="nox -s dependency:audit -- -- [options]",
        )
        parser.add_argument(
            "-v",
            "--vulnerability-issues",
            type=argparse.FileType("r"),
            default=None,
            help="JSONL of vulnerabilities (of type `GitHubVulnerabilityIssue`)",
        )
        return parser.parse_args(args=session.posargs)

    @staticmethod
    def _perform_basic_vulnerability_update(
        pkg_tracker: PackageVersionTracker, vuln_tracker: VulnerabilityTracker
    ) -> None:
        vuln_packages = vuln_tracker.get_packages()

        # vulnerabilities of direct dependencies require a pyproject.toml update
        vuln_direct_dependencies = vuln_packages.intersection(pkg_tracker.packages)
        if vuln_direct_dependencies:
            command = ("poetry", "up") + tuple(vuln_direct_dependencies)
            subprocess.run(command, capture_output=True)

        command = ("poetry", "update") + tuple(vuln_packages)
        subprocess.run(command, capture_output=True)

    def run(self, session: Session) -> DependencyChanges:
        """Update the dependencies associated with GitHubVulnerabilityIssues"""
        args = self._parse_args(session)
        with PackageVersionTracker() as pkg_tracker:
            with VulnerabilityTracker(args.vulnerability_issues) as vuln_tracker:
                self._perform_basic_vulnerability_update(
                    pkg_tracker=pkg_tracker, vuln_tracker=vuln_tracker
                )

        return DependencyChanges(
            package_changes=pkg_tracker.changes,
            issues_resolved=vuln_tracker.issues_resolved,
            issues_not_resolved=vuln_tracker.issues_not_resolved,
            vulnerabilities_resolved=vuln_tracker.vulnerabilities_resolved,
            vulnerabilities_resolved_summary=vuln_tracker.summary,
        )


@nox.session(name="dependency:licenses", python=False)
def dependency_licenses(session: Session) -> None:
    """returns the packages and their licenses"""
    toml = Path("pyproject.toml")
    dependencies = _dependencies(toml.read_text())
    package_infos = _licenses()
    print(_packages_to_markdown(dependencies=dependencies, packages=package_infos))


@nox.session(name="dependency:audit", python=False)
def audit(session: Session) -> None:
    """Check for known vulnerabilities"""
    Audit().run(session=session)


@nox.session(name="dependency:update", python=False)
def update(session: Session) -> None:
    """Updates dependencies & returns changes"""
    dependency_changes = DependencyUpdate().run(session)
    print("Resolved issues")
    print(*dependency_changes.issues_resolved, sep="\n")
    print("\nNot resolved issues")
    print(*dependency_changes.issues_not_resolved, sep="\n")
    print("\nSummary")
    print(*dependency_changes.vulnerabilities_resolved_summary, sep="\n")
    print("\nSecurity fixes")
    print(*dependency_changes.vulnerabilities_resolved, sep="\n")
    print("\nDependencies")
    print(*dependency_changes.package_changes, sep="\n")
