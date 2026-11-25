from __future__ import annotations

from collections.abc import (
    Iterable,
)

import nox
from nox import Session

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._shared import (
    ArgparseResults,
    _integration_test_context,
    _unit_test_context,
)
from exasol.toolbox.nox.plugin import NoxTasks
from noxconfig import (
    PROJECT_CONFIG,
)


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
    print(argparse_results.known.directories)
    return (
        coverage_command
        + ["pytest", *argparse_results.known.directories]
        + argparse_results.other
    )


def _unit_tests(
    session: Session, config: BaseConfig, argeparse_results: ArgparseResults
) -> None:
    command = _test_command(config, argeparse_results)
    session.run(*command)


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


def _coverage(
    session: Session, config: BaseConfig, argeparse_result: ArgparseResults
) -> None:
    command = ["coverage", "report", "-m"]
    coverage_file = config.root_path / ".coverage"
    coverage_file.unlink(missing_ok=True)
    _unit_tests(session, config, argeparse_result)
    _integration_tests(session, config, argeparse_result)
    session.run(*command)


@nox.session(name="test:unit", python=False)
def unit_tests(session: Session) -> None:
    """Runs all unit tests"""
    argeparse_result = _unit_test_context(session)
    _unit_tests(session, PROJECT_CONFIG, argeparse_result)


@nox.session(name="test:integration", python=False)
def integration_tests(session: Session) -> None:
    """
    Runs the all integration tests

    If a project needs to execute code pre-/post the test execution,
    it should provide appropriate hooks on their config object.
        * pre_integration_tests_hook(session: Session, config: Config, context: MutableMapping[str, Any]) -> bool:
        * post_integration_tests_hook(session: Session, config: Config, context: MutableMapping[str, Any]) -> bool:
    """
    argeparse_result = _integration_test_context(session)
    _integration_tests(session, PROJECT_CONFIG, argeparse_result)


@nox.session(name="test:coverage", python=False)
def coverage(session: Session) -> None:
    """Runs all tests (unit + integration) and reports the code coverage"""
    argeparse_result = _integration_test_context(session)
    argeparse_result.known.coverage = True
    _coverage(session, PROJECT_CONFIG, argeparse_result)
