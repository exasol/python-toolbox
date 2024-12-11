import json

import nox
from nox import Session


def _python_matrix():
    return {"python-version": ["3.9", "3.10", "3.11", "3.12"]}


def _exasol_matrix():
    return {"exasol-version": ["7.1.9"]}


@nox.session(name="matrix:python", python=False)
def python_matrix(session: Session) -> None:
    """Output the build matrix for Python versions as JSON."""
    print(json.dumps(_python_matrix()))


@nox.session(name="matrix:exasol", python=False)
def exasol_matrix(session: Session) -> None:
    """Output the build matrix for Exasol versions as JSON."""
    print(json.dumps(_exasol_matrix()))


@nox.session(name="matrix:all", python=False)
def full_matrix(session: Session) -> None:
    """Output the full build matrix for Python & Exasol versions as JSON."""
    matrix = _python_matrix()
    matrix.update(_exasol_matrix())
    print(json.dumps(matrix))
