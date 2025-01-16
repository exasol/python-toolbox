import pytest

from exasol.toolbox.nox._dependencies import (
    Package,
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
        ("BSD License; MIT License;", "BSD"),
        ("MIT License; Mozilla Public License 2.0 (MPL 2.0)", "MIT"),
        (
            "Mozilla Public License 2.0 (MPL 2.0); GNU Lesser General Public License v2 (LGPLv2)",
            "MPLv2",
        ),
        (
            "GNU Lesser General Public License v2 (LGPLv2); GNU General Public License v2 (GPLv2)",
            "LGPLv2",
        ),
        (
            "GNU General Public License v2 (GPLv2); GNU General Public License v3 (GPLv3)",
            "GPLv2",
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
        "License": "MIT License",
        "Name": "pip",
        "URL": "https://pip.pypa.io/",
        "Version": "24.3.1"
    },
    {
        "License": "MIT License",
        "Name": "pip-licenses",
        "URL": "https://github.com/raimon49/pip-licenses",
        "Version": "5.0.0"
    }
]
            """,
            [
                Package(
                    name="pip",
                    version="24.3.1",
                    package_link="https://pip.pypa.io/",
                    license="MIT",
                    license_link="",
                ),
                Package(
                    name="pip-licenses",
                    version="5.0.0",
                    package_link="https://github.com/raimon49/pip-licenses",
                    license="MIT",
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
            """# Dependecies
---

## Project Dependencies
---
|Package|version|Licence|
|---|---|---|
|[package1](package_link1)|version1|[license1](license_link1)|
|[package3](package_link3)|version3|license3|

## Dev Dependencies
---
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
