from collections import defaultdict
from dataclasses import dataclass
from typing import (
    Dict,
    Iterable,
    List,
    Tuple,
)


@dataclass(frozen=True)
class Package:
    name: str
    license: str
    version: str


def _packages(package_info):
    for p in package_info:
        kwargs = {key.lower(): value for key, value in p.items()}
        yield Package(**kwargs)


def _normalize(license):
    def is_mulit_license(l):
        return ";" in l

    def select_most_permissive(l):
        licenses = [_normalize(l.strip()) for l in l.split(";")]
        priority = defaultdict(
            lambda: 9999,
            {"Unlicense": 0, "BSD": 1, "MIT": 2, "MPLv2": 3, "LGPLv2": 4, "GPLv2": 5},
        )
        priority_to_license = defaultdict(
            lambda: "Unknown", {v: k for k, v in priority.items()}
        )
        selected = min(*[priority[lic] for lic in licenses])
        return priority_to_license[selected]

    mapping = {
        "BSD License": "BSD",
        "MIT License": "MIT",
        "The Unlicense (Unlicense)": "Unlicense",
        "Mozilla Public License 2.0 (MPL 2.0)": "MPLv2",
        "GNU Lesser General Public License v2 (LGPLv2)": "LGPLv2",
        "GNU General Public License v2 (GPLv2)": "GPLv2",
    }
    if is_mulit_license(license):
        return select_most_permissive(license)

    if license not in mapping:
        return license

    return mapping[license]


def audit(
    licenses: List[Dict[str, str]], acceptable: List[str], exceptions: Dict[str, str]
) -> Tuple[List[Package], List[Package]]:
    """
    Audit package licenses.

    Args:
        licenses: a list of dictionaries containing license information for packages.
                  This information e.g. can be obtained by running `pip-licenses --format=json`.

            example: [{"License": "BSD License", "Name": "Babel", "Version": "2.12.1"}, ...]

        acceptable: A list of licenses which shall be accepted.
            example: ["BSD License", "MIT License", ...]

        exceptions: A dictionary containing package names and justifications for packages to ignore/skip.
            example: {'packagename': 'justification why this is/can be an exception'}

    Returns:
        Two lists containing found violations and ignored packages.
    """
    packages = list(_packages(licenses))
    acceptable = [_normalize(a) for a in acceptable]
    ignored = [p for p in packages if p.name in exceptions and exceptions[p.name]]
    violations = [
        p
        for p in packages
        if _normalize(p.license) not in acceptable and p not in ignored
    ]
    return violations, ignored
