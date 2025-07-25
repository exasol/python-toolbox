from typing import Optional

import pytest

from exasol.toolbox.util.dependencies.licenses import (
    LICENSE_MAPPING_TO_URL,
    PackageLicense,
    PackageLicenseReport,
    _normalize,
    _packages_from_json,
)


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


def test_packages_from_json():
    json = """[
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
    """

    actual = _packages_from_json(json)

    assert actual == {
        "name1": PackageLicense(
            name="name1",
            version="0.1.0",
            package_link="link1",
            license="license1",
        ),
        "name2": PackageLicense(
            name="name2",
            version="0.2.0",
            package_link=None,
            license="license2",
        ),
    }


@pytest.fixture(scope="module")
def package_license_report(dependencies):
    licenses = {
        "package1": PackageLicense(
            name="package1",
            package_link="package_link1",
            version="0.1.0",
            license="GPLv1",
        ),
        "package2": PackageLicense(
            name="package3",
            package_link="UNKNOWN",
            version="0.3.0",
            license="license3",
        ),
    }

    return PackageLicenseReport(dependencies=dependencies, licenses=licenses)


class TestPackageLicenseReport:
    @staticmethod
    def test_format_group_table_header(package_license_report, main_group):
        result = package_license_report._format_group_table_header(
            group=main_group.name
        )

        assert (
            result == "## `main` Dependencies\n|Package|Version|License|\n|---|---|---|"
        )

    @staticmethod
    def test_format_group_table(package_license_report, dependencies, main_group):
        group_package_names = set(dependencies[main_group.name].keys())

        result = package_license_report._format_group_table(
            group=main_group.name, group_package_names=group_package_names
        )

        assert result == (
            "## `main` Dependencies\n"
            "|Package|Version|License|\n"
            "|---|---|---|\n"
            "|[package1](package_link1)|0.1.0|[GPLv1](https://www.gnu.org/licenses/old-licenses/gpl-1.0.html)|\n"
            "\n"
        )

    @staticmethod
    @pytest.mark.parametrize(
        "package_link,license_link,expected",
        [
            pytest.param(
                "package_link2",
                "GPLv2",
                "|[package2](package_link2)|0.2.0|[GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)|\n",
                id="has-all-attributes",
            ),
            pytest.param(
                None,
                "GPLv2",
                "|package2|0.2.0|[GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)|\n",
                id="no-package-link",
            ),
            pytest.param(
                "package_link2",
                "abcd",
                "|[package2](package_link2)|0.2.0|abcd|\n",
                id="no-associated-license-link",
            ),
        ],
    )
    def test_format_table_row(
        package_license_report,
        package_link: Optional[str],
        license_link: Optional[str],
        expected,
    ):
        _license = PackageLicense(
            name="package2",
            package_link=package_link,
            version="0.2.0",
            license=license_link,
        )
        result = package_license_report._format_table_row(license_info=_license)

        assert result == expected

    @staticmethod
    def test_to_markdown(package_license_report):
        result = package_license_report.to_markdown()
        assert result == (
            "# Dependencies\n"
            "\n"
            "## `main` Dependencies\n"
            "|Package|Version|License|\n"
            "|---|---|---|\n"
            "|[package1](package_link1)|0.1.0|[GPLv1](https://www.gnu.org/licenses/old-licenses/gpl-1.0.html)|\n"
            "\n"
            "## `dev` Dependencies\n"
            "|Package|Version|License|\n"
            "|---|---|---|\n"
            "|package3|0.3.0|license3|"
        )
