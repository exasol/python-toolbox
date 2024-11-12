from __future__ import annotations

from pathlib import Path
from typing import (
    Any,
    Iterable,
    MutableMapping,
)

import nox
from nox import Session

from exasol.toolbox.nox._shared import _context
from exasol.toolbox.nox.plugin import NoxTasks
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)


def _test_command(
    path: Path, config: Config, context: MutableMapping[str, Any]
) -> Iterable[str]:
    base_command = ["poetry", "run"]
    coverage_command = (
        ["coverage", "run", "-a", f"--rcfile={config.root / 'pyproject.toml'}", "-m"]
        if context["coverage"]
        else []
    )
    pytest_command = ["pytest", "-v", f"{path}"]
    return base_command + coverage_command + pytest_command + context["fwd-args"]


def _unit_tests(
    session: Session, config: Config, context: MutableMapping[str, Any]
) -> None:
    command = _test_command(config.root / "test" / "unit", config, context)
    session.run(*command)


def _integration_tests(
    session: Session, config: Config, context: MutableMapping[str, Any]
) -> None:
    pm = NoxTasks.plugin_manager(config)

    # run pre intergration test plugins
    pm.hook.pre_integration_tests_hook(session=session, config=config, context={})

    # run
    command = _test_command(config.root / "test" / "integration", config, context)
    session.run(*command)

    # run post intergration test plugins
    pm.hook.post_integration_tests_hook(session=session, config=config, context={})


def _pass(
    _session: Session, _config: Config, _context: MutableMapping[str, Any]
) -> bool:
    """No operation"""
    return True


def _coverage(
    session: Session, config: Config, context: MutableMapping[str, Any]
) -> None:
    command = ["poetry", "run", "coverage", "report", "-m"]
    coverage_file = config.root / ".coverage"
    coverage_file.unlink(missing_ok=True)
    _unit_tests(session, config, context)
    _integration_tests(session, config, context)
    session.run(*command)


@nox.session(name="test:unit", python=False)
def unit_tests(session: Session) -> None:
    """Runs all unit tests"""
    context = _context(session, coverage=False)
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
    context = _context(session, coverage=False)
    _integration_tests(session, PROJECT_CONFIG, context)


@nox.session(name="test:coverage", python=False)
def coverage(session: Session) -> None:
    """Runs all tests (unit + integration) and reports the code coverage"""
    context = _context(session, coverage=True)
    _coverage(session, PROJECT_CONFIG, context)
