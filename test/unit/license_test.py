import pytest

from exasol.toolbox.license import audit


@pytest.fixture
def licenses():
    yield [
        {"License": "BSD License", "Name": "Babel", "Version": "2.12.1"},
        {"License": "MIT License", "Name": "PyYAML", "Version": "6.0"},
        {
            "License": "Apache Software License",
            "Name": "argcomplete",
            "Version": "2.1.2",
        },
        {
            "License": "GNU Lesser General Public License v2 (LGPLv2)",
            "Name": "astroid",
            "Version": "2.15.5",
        },
        {
            "License": "Mozilla Public License 2.0 (MPL 2.0)",
            "Name": "certifi",
            "Version": "2023.5.7",
        },
        {
            "License": "Python Software Foundation License",
            "Name": "distlib",
            "Version": "0.3.6",
        },
        {
            "License": "BSD License; GNU General Public License (GPL); Public Domain; Python Software Foundation License",
            "Name": "docutils",
            "Version": "0.19",
        },
        {
            "License": "The Unlicense (Unlicense)",
            "Name": "filelock",
            "Version": "3.12.2",
        },
        {
            "License": "Mozilla Public License 2.0 (MPL 2.0)",
            "Name": "pathspec",
            "Version": "0.11.1",
        },
        {
            "License": "GNU General Public License (GPL); GNU General Public License v2 or later (GPLv2+); Other/Proprietary License",
            "Name": "prysk",
            "Version": "0.15.1",
        },
        {
            "License": "GNU General Public License v2 (GPLv2)",
            "Name": "pylint",
            "Version": "2.17.4",
        },
    ]


def test_nothing_to_validate():
    licenses = []
    acceptable = []
    exceptions = []
    violations, exceptions = audit(licenses, acceptable, exceptions)
    assert set(violations) == set()
    assert set(exceptions) == set()


@pytest.mark.parametrize(
    "acceptable,exceptions,expected_violations,expected_exceptions",
    [
        ([], [], 11, 0),
        (["BSD License", "MIT License"], {}, 8, 0),
        (
            ["BSD License", "MIT License"],
            {"prysk": "Prysk is only a development dependency"},
            7,
            1,
        ),
    ],
)
def test_audit(
    licenses, acceptable, exceptions, expected_violations, expected_exceptions
):
    violations, exceptions = audit(
        licenses, acceptable=acceptable, exceptions=exceptions
    )
    assert len(violations) == expected_violations
    assert len(exceptions) == expected_exceptions
