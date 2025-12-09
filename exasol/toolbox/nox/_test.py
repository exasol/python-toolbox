from __future__ import annotations

from collections.abc import (
    Iterable,
    MutableMapping,
)
from pathlib import Path
from typing import Any

import nox
from nox import Session

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._shared import _context
from exasol.toolbox.nox.plugin import NoxTasks
from noxconfig import (
    PROJECT_CONFIG,
)


def _test_command(
    path: Path, config: BaseConfig, context: MutableMapping[str, Any]
) -> Iterable[str]:
    coverage_command = (
        [
            "coverage",
            "run",
            "-a",
            f"--rcfile={config.root_path / 'pyproject.toml'}",
            "-m",
        ]
        if context["coverage"]
        else []
    )
    pytest_command = ["pytest", "-v", f"{path}"]
    return coverage_command + pytest_command + context["fwd-args"]


def _unit_tests(
    session: Session, config: BaseConfig, context: MutableMapping[str, Any]
) -> None:
    command = _test_command(config.root_path / "test" / "unit", config, context)
    session.run(*command)


def _integration_tests(
    session: Session, config: BaseConfig, context: MutableMapping[str, Any]
) -> None:
    pm = NoxTasks.plugin_manager(config)

    # run pre integration test plugins
    pm.hook.pre_integration_tests_hook(session=session, config=config, context=context)

    # Notes:
    # - Catch exceptions and ensure post-hooks run before exiting
    # - Consider making the executed command(s) configurable via a plugin hook
    #   (The default implementation of the hook could provide the current implementation)
    command = _test_command(config.root_path / "test" / "integration", config, context)
    session.run(*command)

    # run post integration test plugins
    pm.hook.post_integration_tests_hook(session=session, config=config, context=context)


def _coverage(
    session: Session, config: BaseConfig, context: MutableMapping[str, Any]
) -> None:
    command = ["coverage", "report", "-m"]
    coverage_file = config.root_path / ".coverage"
    coverage_file.unlink(missing_ok=True)
    _unit_tests(session, config, context)
    _integration_tests(session, config, context)
    session.run(*command)


@nox.session(name="test:unit", python=False)
def unit_tests(session: Session) -> None:
    """Runs all unit tests"""
    context = _context(session)
    _unit_tests(session, PROJECT_CONFIG, context)


@nox.session(name="test:integration", python=False)
def integration_tests(session: Session) -> None:
    """
    Runs the all integration tests

    If a project needs to execute code pre-/post the test execution,
    it should provide appropriate hooks on their config object.
        * pre_integration_tests_hook(session: Session, config: Config, context: MutableMapping[str, Any]) -> bool:
        * post_integration_tests_hook(session: Session, config: Config, context: MutableMapping[str, Any]) -> bool:
    """
    context = _context(session)
    _integration_tests(session, PROJECT_CONFIG, context)


@nox.session(name="test:coverage", python=False)
def coverage(session: Session) -> None:
    """Runs all tests (unit + integration) and reports the code coverage"""
    context = _context(session, coverage=True)
    _coverage(session, PROJECT_CONFIG, context)
