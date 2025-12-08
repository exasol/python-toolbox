import shutil
from unittest.mock import patch

import pytest

from exasol.toolbox.nox._test import (
    _test_command,
    integration_tests,
    unit_tests,
)
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def default_context():
    """
    The default context comes from  `toolbox/nox/_shared.py::_context`
    """
    return {"db_version": "7.1.9", "coverage": False, "fwd-args": []}


class TestTestCommand:
    @staticmethod
    def test_works_for_default_arguments(test_project_config_factory, default_context):
        config = test_project_config_factory()

        result = _test_command(
            path=config.root_path / "dummy", config=config, context=default_context
        )

        assert result == ["pytest", "-v", f"{config.root_path}/dummy"]

    @staticmethod
    def test_works_for_coverage_true(test_project_config_factory, default_context):
        config = test_project_config_factory()
        default_context["coverage"] = True

        result = _test_command(
            path=config.root_path / "dummy", config=config, context=default_context
        )

        assert result == [
            "coverage",
            "run",
            "-a",
            f"--rcfile={config.root_path}/pyproject.toml",
            "-m",
            "pytest",
            "-v",
            f"{config.root_path}/dummy",
        ]

    @staticmethod
    def test_works_for_fwd_args(test_project_config_factory, default_context):
        config = test_project_config_factory()
        default_context["fwd-args"] = ["--addition"]

        result = _test_command(
            path=config.root_path / "dummy", config=config, context=default_context
        )

        assert result == ["pytest", "-v", f"{config.root_path}/dummy", "--addition"]


def test_unit_tests(nox_session, test_project_config_factory):
    config = test_project_config_factory()

    shutil.copyfile(
        PROJECT_CONFIG.root_path / "pyproject.toml", config.root_path / "pyproject.toml"
    )

    test_directory = config.root_path / "test" / "unit"
    test_directory.mkdir(parents=True, exist_ok=True)
    test_filepath = test_directory / "dummy_test.py"
    test_filepath.write_text("def test_dummy():\n    assert True")

    with patch("exasol.toolbox.nox._test.PROJECT_CONFIG", new=config):
        unit_tests(nox_session)

    assert (test_directory / "__pycache__").exists()


class TestIntegrationTests:
    @staticmethod
    def test_works_without_hooks(nox_session, test_project_config_factory):
        config = test_project_config_factory()

        shutil.copyfile(
            PROJECT_CONFIG.root_path / "pyproject.toml",
            config.root_path / "pyproject.toml",
        )

        test_directory = config.root_path / "test" / "integration"
        test_directory.mkdir(parents=True, exist_ok=True)
        test_filepath = test_directory / "dummy_test.py"
        test_filepath.write_text("def test_dummy():\n    assert True")

        with patch("exasol.toolbox.nox._test.PROJECT_CONFIG", new=config):
            integration_tests(nox_session)

        assert (test_directory / "__pycache__").exists()
