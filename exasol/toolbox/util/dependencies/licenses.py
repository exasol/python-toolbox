from __future__ import annotations

import subprocess
import tempfile
from inspect import cleandoc
from json import loads
from typing import Optional

from pydantic import field_validator

from exasol.toolbox.util.dependencies.shared_models import Package

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


def _packages_from_json(json: str) -> list[PackageLicense]:
    packages = loads(json)
    return [
        PackageLicense(
            name=package["Name"],
            package_link=package["URL"],
            version=package["Version"],
            license=package["License"],
        )
        for package in packages
    ]


def licenses() -> list[PackageLicense]:
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


def packages_to_markdown(
    dependencies: dict[str, list], packages: list[PackageLicense]
) -> str:
    def heading():
        return "# Dependencies\n"

    def dependency(
        group: str,
        group_packages: list[Package],
        packages: list[PackageLicense],
    ) -> str:
        def _header(_group: str):
            _group = "".join([word.capitalize() for word in _group.strip().split()])
            text = f"## {_group} Dependencies\n"
            text += "|Package|Version|License|\n"
            text += "|---|---|---|\n"
            return text

        def _rows(
            _group_packages: list[Package], _packages: list[PackageLicense]
        ) -> str:
            text = ""
            for package in _group_packages:
                consistent = filter(
                    lambda elem: elem.normalized_name == package.normalized_name,
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
