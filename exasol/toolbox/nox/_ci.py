import json
import logging

import nox
from nox import Session

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._shared import check_for_config_attribute
from noxconfig import (
    PROJECT_CONFIG,
)

_log = logging.getLogger(__name__)


def _python_matrix(config: BaseConfig):
    check_for_config_attribute(config=config, attribute="python_versions")
    return {"python-version": config.python_versions}


def _exasol_matrix(config: BaseConfig):
    check_for_config_attribute(config=config, attribute="exasol_versions")
    return {"exasol-version": config.exasol_versions}


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
