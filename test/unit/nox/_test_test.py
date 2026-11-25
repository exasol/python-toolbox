from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock

import pytest

from exasol.toolbox.nox._test import (
    INTEGRATION_TESTS_DIRECTORY,
    UNIT_TESTS_DIRECTORY,
    ArgparseResults,
    _integration_test_context,
    _test_command,
    _unit_test_context,
)
from noxconfig import PROJECT_CONFIG

PATH_CASES = [
    ([], []),
    (["abc"], []),
    (["abc", "def"], []),
    ([], ["-s"]),
    ([], ["-k", "TestClass"]),
    (["abc"], ["-k", "TestClass"]),
    (["abc", "def"], ["-v"]),
]


def _posargs(dirs, other):
    if not dirs:
        return other
    return ["--paths", *dirs] + other


class TestUnitTestContext:
    @staticmethod
    @pytest.mark.parametrize("dirs, other", PATH_CASES)
    def test_paths_and_other_arguments(dirs, other):
        result = _unit_test_context(Mock(posargs=_posargs(dirs, other)))

        assert result == ArgparseResults(
            known=Namespace(
                paths=[Path(d) for d in dirs] or [UNIT_TESTS_DIRECTORY],
                coverage=False,
            ),
            other=other,
        )

    @staticmethod
    @pytest.mark.parametrize(
        "flags, attribute, expected",
        [
            (["--coverage"], "coverage", True),
        ],
    )
    def test_overrides_default(flags, attribute, expected):
        default = getattr(_unit_test_context(Mock(posargs=[])).known, attribute)

        result = _unit_test_context(Mock(posargs=flags))

        assert getattr(result.known, attribute) == expected
        assert getattr(result.known, attribute) != default


class TestIntegrationTestContext:
    @staticmethod
    @pytest.mark.parametrize("dirs, other", PATH_CASES)
    def test_paths_and_other_arguments(dirs, other):
        result = _integration_test_context(Mock(posargs=_posargs(dirs, other)))

        assert result == ArgparseResults(
            known=Namespace(
                paths=[Path(d) for d in dirs] or [INTEGRATION_TESTS_DIRECTORY],
                coverage=False,
                db_version=PROJECT_CONFIG.minimum_exasol_version,
            ),
            other=other,
        )

    @staticmethod
    @pytest.mark.parametrize(
        "flags, attribute, expected",
        [
            (["--coverage"], "coverage", True),
            (["--db-version", "8.0.0"], "db_version", "8.0.0"),
        ],
    )
    def test_overrides_default(flags, attribute, expected):
        default = getattr(_integration_test_context(Mock(posargs=[])).known, attribute)

        result = _integration_test_context(Mock(posargs=flags))

        assert getattr(result.known, attribute) == expected
        assert getattr(result.known, attribute) != default


class TestTestCommand:
    @staticmethod
    def test_without_coverage(test_project_config_factory):
        config = test_project_config_factory()
        argparse_results = ArgparseResults(
            known=Namespace(paths=[config.root_path / "dummy"], coverage=False),
            other=["-v"],
        )

        result = _test_command(config=config, argparse_results=argparse_results)

        assert result == ["pytest", config.root_path / "dummy", "-v"]

    @staticmethod
    def test_with_coverage(test_project_config_factory):
        config = test_project_config_factory()
        argparse_results = ArgparseResults(
            known=Namespace(paths=[config.root_path / "dummy"], coverage=True),
            other=["-v"],
        )

        result = _test_command(config=config, argparse_results=argparse_results)

        assert result == [
            "coverage",
            "run",
            "-a",
            f"--rcfile={config.root_path}/pyproject.toml",
            "-m",
            "pytest",
            config.root_path / "dummy",
            "-v",
        ]
