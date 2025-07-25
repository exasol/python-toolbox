from __future__ import annotations

import subprocess
import tempfile
from collections import OrderedDict
from dataclasses import dataclass
from inspect import cleandoc
from json import loads
from typing import Optional

from pydantic import field_validator

from exasol.toolbox.util.dependencies.shared_models import (
    NormalizedPackageStr,
    Package,
)

LICENSE_MAPPING_TO_ABBREVIATION = {
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

LICENSE_MAPPING_TO_URL = {
    "GPLv1": "https://www.gnu.org/licenses/old-licenses/gpl-1.0.html",
    "GPLv2": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
    "LGPLv2": "https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html",
    "GPLv3": "https://www.gnu.org/licenses/gpl-3.0.html",
    "LGPLv3": "https://www.gnu.org/licenses/lgpl-3.0.html",
    "Apache": "https://www.apache.org/licenses/LICENSE-2.0",
    "MIT": "https://mit-license.org/",
    "BSD": "https://opensource.org/license/bsd-3-clause",
}


class PackageLicense(Package):
    package_link: Optional[str]
    license: str

    @field_validator("package_link", mode="before")
    def map_unknown_to_none(cls, v) -> Optional[str]:
        if v == "UNKNOWN":
            return None
        return v

    @field_validator("license", mode="before")
    def map_to_normalized_values(cls, v) -> Optional[str]:
        return _normalize(v)

    @property
    def license_link(self) -> Optional[str]:
        return LICENSE_MAPPING_TO_URL.get(self.license, None)


def _normalize(_license: str) -> str:
    def is_multi_license(l: str) -> bool:
        return ";" in l

    def select_most_restrictive(licenses: list[str]) -> str:
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

    if is_multi_license(_license):
        items = []
        for item in _license.split(";"):
            item = str(item).strip()
            items.append(LICENSE_MAPPING_TO_ABBREVIATION.get(item, item))
        return select_most_restrictive(items)

    return LICENSE_MAPPING_TO_ABBREVIATION.get(_license, _license)


def _packages_from_json(json: str) -> dict[NormalizedPackageStr, PackageLicense]:
    packages = loads(json)
    return {
        package_license.normalized_name: package_license
        for package in packages
        if (
            package_license := PackageLicense(
                name=package["Name"],
                package_link=package["URL"],
                version=package["Version"],
                license=package["License"],
            )
        )
    }


def get_licenses() -> dict[NormalizedPackageStr, PackageLicense]:
    with tempfile.NamedTemporaryFile() as file:
        subprocess.run(
            [
                "pip-licenses",
                "--format=json",
                "--output-file=" + file.name,
                "--with-system",
                "--with-urls",
            ],
            capture_output=True,
            check=True,
        )
        return _packages_from_json(file.read().decode())


@dataclass(frozen=True)
class PackageLicenseReport:
    dependencies: OrderedDict[str, dict[NormalizedPackageStr, Package]]
    licenses: dict[NormalizedPackageStr, PackageLicense]

    @staticmethod
    def _format_group_table_header(group: str) -> str:
        return cleandoc(
            f"""## `{group}` Dependencies
            |Package|Version|License|
            |---|---|---|
            """
        )

    def _format_group_table(
        self, group: str, group_package_names: set[NormalizedPackageStr]
    ) -> str:
        group_header = self._format_group_table_header(group=group)

        rows = []
        for package_name in sorted(group_package_names):
            if license_info := self.licenses.get(package_name):
                rows.append(self._format_table_row(license_info=license_info))

        return f"""{group_header}\n{''.join(rows)}\n"""

    @staticmethod
    def _format_table_row(license_info: PackageLicense) -> str:
        row_package = f"{license_info.name}"
        if license_info.package_link:
            row_package = f"[{license_info.name}]({license_info.package_link})"

        row_license = f"{license_info.license}"
        if license_info.license_link:
            row_license = f"[{license_info.license}]({license_info.license_link})"

        return f"|{row_package}|{license_info.version}|{row_license}|\n"

    def to_markdown(self) -> str:
        rows = []
        for group in self.dependencies:
            group_package_names = set(self.dependencies[group].keys())
            rows.append(
                self._format_group_table(
                    group=group, group_package_names=group_package_names
                )
            )
        return cleandoc(f"""# Dependencies\n\n{''.join(rows)}""")
