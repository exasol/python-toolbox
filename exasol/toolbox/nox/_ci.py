import json
import logging

import nox
from nox import Session

from noxconfig import (
    PROJECT_CONFIG,
    Config,
)

_log = logging.getLogger(__name__)

_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]
_EXASOL_VERSIONS = ["7.1.9"]


def _python_matrix(config: Config):
    attr = "python_versions"
    python_versions = getattr(config, attr, _PYTHON_VERSIONS)
    if not hasattr(config, attr):
        _log.warning(
            "Config does not contain '%s' setting. Using default: %s",
            attr,
            _PYTHON_VERSIONS,
        )
    return {"python-version": python_versions}


def _exasol_matrix(config: Config):
    attr = "exasol_versions"
    exasol_versions = getattr(config, attr, _EXASOL_VERSIONS)
    if not hasattr(config, attr):
        _log.warning(
            "Config does not contain '%s' setting. Using default: %s",
            attr,
            _EXASOL_VERSIONS,
        )
    return {"exasol-version": exasol_versions}


@nox.session(name="matrix:python", python=False)
def python_matrix(session: Session) -> None:
    """Output the build matrix for Python versions as JSON."""
    print(json.dumps(_python_matrix(PROJECT_CONFIG)))


@nox.session(name="matrix:exasol", python=False)
def exasol_matrix(session: Session) -> None:
    """Output the build matrix for Exasol versions as JSON."""
    print(json.dumps(_exasol_matrix(PROJECT_CONFIG)))


@nox.session(name="matrix:all", python=False)
def full_matrix(session: Session) -> None:
    """Output the full build matrix for Python & Exasol versions as JSON."""
    matrix = _python_matrix(PROJECT_CONFIG)
    matrix.update(_exasol_matrix(PROJECT_CONFIG))
    print(json.dumps(matrix))
