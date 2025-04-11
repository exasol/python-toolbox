from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from dataclasses import dataclass
from inspect import cleandoc
from json import loads
from pathlib import Path

import nox
import tomlkit
from nox import Session


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
        dependencies["project"] = []
    for package in packages:
        dependencies["project"].append(package)

    packages = poetry.get("dev", {}).get("dependencies", {})
    if packages:
        dependencies["dev"] = []
    for package in packages:
        dependencies["dev"].append(package)

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
    """returns the packages and their licenses"""
    toml = Path("pyproject.toml")
    dependencies = _dependencies(toml.read_text())
    package_infos = _licenses()
    print(_packages_to_markdown(dependencies=dependencies, packages=package_infos))


@nox.session(name="dependency:audit", python=False)
def audit(session: Session) -> None:
    """Check for known vulnerabilities"""
    Audit().run(session=session)
