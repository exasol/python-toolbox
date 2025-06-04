import pytest

from exasol.toolbox.util.dependencies.licenses import (
    LICENSE_MAPPING_TO_URL,
    PackageLicense,
    _normalize,
    _packages_from_json,
    packages_to_markdown,
)
from exasol.toolbox.util.dependencies.poetry_dependencies import PoetryGroup
from exasol.toolbox.util.dependencies.shared_models import Package

MAIN_GROUP = PoetryGroup(name="main", toml_section="project.dependencies")
DEV_GROUP = PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies")


class TestPackageLicense:
    @staticmethod
    def test_package_link_map_unknown_to_none():
        result = PackageLicense(
            name="dummy", version="0.1.0", package_link="UNKNOWN", license="dummy"
        )
        assert result.package_link is None

    @staticmethod
    @pytest.mark.parametrize(
        "license,expected",
        [
            ("GPLv1", LICENSE_MAPPING_TO_URL["GPLv1"]),
            ("DUMMY", None),
        ],
    )
    def test_license_link(license, expected):
        result = PackageLicense(
            name="dummy", version="0.1.0", package_link="dummy", license=license
        )
        assert result.license_link == expected


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
                        "Version": "0.1.0"
                    },
                    {
                        "License": "license2",
                        "Name": "name2",
                        "URL": "UNKNOWN",
                        "Version": "0.2.0"
                    }
                ]
                            """,
            [
                PackageLicense(
                    name="name1",
                    version="0.1.0",
                    package_link="link1",
                    license="license1",
                ),
                PackageLicense(
                    name="name2",
                    version="0.2.0",
                    package_link=None,
                    license="license2",
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
                    Package(name="package1", version="0.1.0"),
                    Package(name="package3", version="0.1.0"),
                ],
                DEV_GROUP.name: [Package(name="package2", version="0.2.0")],
            },
            [
                PackageLicense(
                    name="package1",
                    package_link="package_link1",
                    version="0.1.0",
                    license="GPLv1",
                ),
                PackageLicense(
                    name="package2",
                    package_link="package_link2",
                    version="0.2.0",
                    license="GPLv2",
                ),
                PackageLicense(
                    name="package3",
                    package_link="UNKNOWN",
                    version="0.3.0",
                    license="license3",
                ),
            ],
        )
    ],
)
def test_packages_to_markdown(dependencies, packages):
    actual = packages_to_markdown(dependencies, packages)
    assert (
        actual
        == """# Dependencies
## Main Dependencies
|Package|Version|License|
|---|---|---|
|[package1](package_link1)|0.1.0|[GPLv1](https://www.gnu.org/licenses/old-licenses/gpl-1.0.html)|
|package3|0.3.0|license3|

## Dev Dependencies
|Package|Version|License|
|---|---|---|
|[package2](package_link2)|0.2.0|[GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)|

"""
    )
