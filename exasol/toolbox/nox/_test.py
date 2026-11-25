from __future__ import annotations

import argparse
from collections.abc import (
    Iterable,
)
from dataclasses import dataclass
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox.plugin import NoxTasks
from noxconfig import PROJECT_CONFIG

UNIT_TESTS_DIRECTORY = PROJECT_CONFIG.root_path / "test" / "unit"
INTEGRATION_TESTS_DIRECTORY = PROJECT_CONFIG.root_path / "test" / "integration"


@dataclass
class ArgparseResults:
    known: argparse.Namespace
    other: list[str]


def _unit_test_context(session: Session) -> ArgparseResults:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        type=Path,
        default=[UNIT_TESTS_DIRECTORY],
        help="Paths (files or directories) to be tested",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    return ArgparseResults(*parser.parse_known_args(session.posargs))


def _integration_test_context(session: Session) -> ArgparseResults:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        type=Path,
        default=[INTEGRATION_TESTS_DIRECTORY],
        help="Paths (files or directories) to be tested",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    parser.add_argument(
        "--db-version",
        default=PROJECT_CONFIG.minimum_exasol_version,
        help="Specify the Exasol DB version to be used",
    )
    return ArgparseResults(*parser.parse_known_args(session.posargs))


def _test_command(
    config: BaseConfig, argparse_results: ArgparseResults
) -> Iterable[str]:
    coverage_command = (
        [
            "coverage",
            "run",
            "-a",
            f"--rcfile={config.root_path / 'pyproject.toml'}",
            "-m",
        ]
        if argparse_results.known.coverage
        else []
    )
    return (
        coverage_command
        + ["pytest", *argparse_results.known.paths]
        + argparse_results.other
    )


def _integration_tests(
    session: Session, config: BaseConfig, argparse_results: ArgparseResults
) -> None:
    pm = NoxTasks.plugin_manager(config)

    # run pre integration test plugins
    pm.hook.pre_integration_tests_hook(
        session=session, config=config, context=argparse_results
    )

    # Notes:
    # - Catch exceptions and ensure post-hooks run before exiting
    # - Consider making the executed command(s) configurable via a plugin hook
    #   (The default implementation of the hook could provide the current implementation)
    command = _test_command(config, argparse_results)
    session.run(*command)

    # run post integration test plugins
    pm.hook.post_integration_tests_hook(
        session=session, config=config, context=argparse_results
    )


@nox.session(name="test:unit", python=False)
def unit_tests(session: Session) -> None:
    """Runs all unit tests"""
    argparse_results = _unit_test_context(session)
    command = _test_command(PROJECT_CONFIG, argparse_results)
    session.run(*command)


@nox.session(name="test:integration", python=False)
def integration_tests(session: Session) -> None:
    """
    Runs the all integration tests

    If a project needs to execute code pre-/post the test execution,
    it should provide appropriate hooks on their config object.
        * pre_integration_tests_hook
        * post_integration_tests_hook
    """
    argparse_results = _integration_test_context(session)
    _integration_tests(session, PROJECT_CONFIG, argparse_results)
