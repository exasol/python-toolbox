from __future__ import annotations

__all__ = [
    "Mode",
    "build_docs",
    "check",
    "clean_docs",
    "coverage",
    "fix",
    "integration_tests",
    "lint",
    "open_docs",
    "prepare_release",
    "type_check",
    "unit_tests",
]


import nox
from nox import Session

from exasol.toolbox.nox._format import (
    _code_format,
    fix,
)

# fmt: off
# isort: off
from noxconfig import PROJECT_CONFIG


@nox.session(name="project:check", python=False)
def check(session: Session) -> None:
    """Runs all available checks on the project"""
    context = _context(session, coverage=True)
    py_files = python_files(PROJECT_CONFIG.root)
    _version(session, Mode.Check)
    _code_format(session, Mode.Check, py_files)
    _pylint(session, py_files)
    _type_check(session, py_files)
    _coverage(session, PROJECT_CONFIG, context)

from exasol.toolbox.nox._metrics import report
from exasol.toolbox.nox._test import (
    _coverage,
    coverage,
    integration_tests,
    unit_tests,
)
from exasol.toolbox.nox._lint import (
    _pylint,
    _type_check,
    lint,
    type_check,
)
from exasol.toolbox.nox._documentation import (
    build_docs,
    clean_docs,
    open_docs,
    updated,
)
from exasol.toolbox.nox._release import prepare_release
from exasol.toolbox.nox._shared import (
    Mode,
    _context,
    _version,
    python_files,
)

from exasol.toolbox.nox._ci import (
    python_matrix,
    exasol_matrix,
    full_matrix,
)

from exasol.toolbox.nox._release import prepare_release

from exasol.toolbox.nox._artifacts import (
    check_artifacts,
    copy_artifacts,
    upload_artifacts_to_sonar
)

from exasol.toolbox.nox._dependencies import (
    dependency_licenses,
    audit
)

from exasol.toolbox.nox._package_version import version_check

# isort: on
# fmt: on
