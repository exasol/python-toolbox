from __future__ import annotations

from collections import defaultdict
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


def _licenses(session: Session, filename: str) -> None:
    session.run(
        "poetry",
        "run",
        "pip-licenses",
        "--format=json",
        "--output-file=" + filename,
        "--with-system",
        "--with-urls",
    )


def _normalize(_license: str) -> str:
    def is_multi_license(l):
        return ";" in l

    def select_most_permissive(l: str) -> str:
        licenses = [_normalize(l.strip()) for l in l.split(";")]
        priority = defaultdict(
            lambda: 9999,
            {
                "Unlicensed": 0,
                "BSD": 1,
                "MIT": 2,
                "MPLv2": 3,
                "LGPLv2": 4,
                "GPLv2": 5,
            },
        )
        priority_to_license = defaultdict(
            lambda: "Unknown", {v: k for k, v in priority.items()}
        )
        selected = min(*[priority[lic] for lic in licenses])
        return priority_to_license[int(selected)]

    mapping = {
        "BSD License": "BSD",
        "MIT License": "MIT",
        "The Unlicensed (Unlicensed)": "Unlicensed",
        "Mozilla Public License 2.0 (MPL 2.0)": "MPLv2",
        "GNU Lesser General Public License v2 (LGPLv2)": "LGPLv2",
        "GNU General Public License v2 (GPLv2)": "GPLv2",
        "GNU General Public License v3 (GPLv3)": "GPLv3",
    }

    if is_multi_license(_license):
        return select_most_permissive(_license)

    if _license not in mapping:
        return _license

    return mapping[_license]


def _packages_from_json(json: str) -> list[Package]:
    packages = loads(json)
    packages_list = []
    for package in packages:
        packages_list.append(
            Package(
                name=package["Name"],
                package_link=package["URL"],
                version=package["Version"],
                license=_normalize(package["License"]),
                license_link="",
            )
        )
    return packages_list


def _packages_to_markdown(
    dependencies: dict[str, list], packages: list[Package]
) -> str:
    def heading():
        text = "# Dependecies\n"
        text += "---\n\n"
        return text

    def dependency(group: str, group_packages: list, packages: list[Package]) -> str:
        def _header(_group: str):
            _group = "".join([word.capitalize() for word in _group.strip().split()])
            text = f"## {_group} Dependencies\n"
            text += "---\n"
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
                    text += f"|[{content.name}]({content.package_link})"
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


@nox.session(name="dependency:licenses", python=False)
def dependency_licenses(session: Session) -> None:
    """returns the packages and their licenses"""
    toml = Path("pyproject.toml")
    dependencies = _dependencies(toml.read_text())
    _licenses(session=session, filename=".packages.json")
    json = Path(".packages.json").read_text()
    package_infos = _packages_from_json(json)
    print(_packages_to_markdown(dependencies=dependencies, packages=package_infos))
