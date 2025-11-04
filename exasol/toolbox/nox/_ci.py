import json
import logging

import nox
from nox import Session

from noxconfig import (
    PROJECT_CONFIG,
    Config,
)

_log = logging.getLogger(__name__)


def check_for_config_attribute(config: Config, attribute: str):
    if not hasattr(config, attribute):
        raise AttributeError(
            "in the noxconfig.py file, the class Config should inherit "
            "from `exasol.toolbox.config.BaseConfig`. This is used to "
            f"set the default `{attribute}`. If the allowed "
            f"`{attribute} needs to differ in your project, you can "
            "set it in the PROJECT_CONFIG statement."
        )


def _python_matrix(config: Config):
    check_for_config_attribute(config=config, attribute="python_versions")
    return {"python-version": config.python_versions}


def _exasol_matrix(config: Config):
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
