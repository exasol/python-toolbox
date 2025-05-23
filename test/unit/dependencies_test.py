import json
from inspect import cleandoc

import pytest
from toolbox.util.dependencies.poetry_dependencies import (
    PoetryDependency,
    PoetryGroup,
)

from exasol.toolbox.nox._dependencies import (
    Audit,
    PackageLicense,
    _normalize,
    _packages_from_json,
    _packages_to_markdown,
)

MAIN_GROUP = PoetryGroup(name="main", toml_section="project.dependencies")
DEV_GROUP = PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies")


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
                PackageLicense(
                    name="name1",
                    version="version1",
                    package_link="link1",
                    license="license1",
                    license_link="",
                ),
                PackageLicense(
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
    "dependencies,packages",
    [
        (
            {
                MAIN_GROUP.name: [
                    PoetryDependency(
                        name="package1", version="version1", group=MAIN_GROUP
                    ),
                    PoetryDependency(
                        name="package3", version="version3", group=MAIN_GROUP
                    ),
                ],
                DEV_GROUP.name: [
                    PoetryDependency(
                        name="package2", version="version2", group=DEV_GROUP
                    )
                ],
            },
            [
                PackageLicense(
                    name="package1",
                    package_link="package_link1",
                    version="version1",
                    license="license1",
                    license_link="license_link1",
                ),
                PackageLicense(
                    name="package2",
                    package_link="package_link2",
                    version="version2",
                    license="license2",
                    license_link="license_link2",
                ),
                PackageLicense(
                    name="package3",
                    package_link="package_link3",
                    version="version3",
                    license="license3",
                    license_link="",
                ),
            ],
        )
    ],
)
def test_packages_to_markdown(dependencies, packages):
    actual = _packages_to_markdown(dependencies, packages)
    assert (
        actual
        == """# Dependencies
## Main Dependencies
|Package|version|Licence|
|---|---|---|
|[package1](package_link1)|version1|[license1](license_link1)|
|[package3](package_link3)|version3|license3|

## Dev Dependencies
|Package|version|Licence|
|---|---|---|
|[package2](package_link2)|version2|[license2](license_link2)|

"""
    )


class TestFilterJsonForVulnerabilities:

    @staticmethod
    def test_no_vulnerability_returns_empty_list():
        audit_dict = {
            "dependencies": [{"name": "alabaster", "version": "0.7.16", "vulns": []}]
        }
        audit_json = json.dumps(audit_dict).encode("utf-8")
        expected = {"dependencies": []}

        actual = Audit._filter_json_for_vulnerabilities(audit_json)
        assert actual == expected

    @staticmethod
    def test_vulnerabilities_returned_in_list(pip_audit_report):
        audit_json = json.dumps(pip_audit_report).encode("utf-8")

        actual = Audit._filter_json_for_vulnerabilities(audit_json)
        assert actual == pip_audit_report
