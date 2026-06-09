import argparse
import json
from collections.abc import Iterable
from typing import Any

import nox
from nox import Session

from exasol.toolbox.config import BaseConfig
from noxconfig import (
    PROJECT_CONFIG,
)

# The relevant nox sessions will be removed in:
#   https://github.com/exasol/python-toolbox/issues/859
MATRIX_DEPRECATION_DATE = "2026-09-15"


def _matrix_keys(config: BaseConfig) -> tuple[str, ...]:
    """
    Return the config keys that are valid for matrix generation.

    Includes both declared fields and computed fields.
    """

    config_class = type(config)
    return tuple(config_class.model_fields) + tuple(config_class.model_computed_fields)


def _matrix_args(session: Session, config: BaseConfig) -> list[str]:
    parser = argparse.ArgumentParser(
        prog="nox -s matrix:generate",
        usage="nox -s matrix:generate -- <config-key> [<config-key> ...]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "keys",
        nargs="+",
        choices=sorted(_matrix_keys(config)),
        help="BaseConfig keys to include in the generated matrix output",
    )
    return parser.parse_args(session.posargs).keys


def _dump_matrix(config: BaseConfig, keys: Iterable[str]) -> dict[str, Any]:
    """
    Build a JSON-serializable matrix subset from the project's config.

    GitHub Actions matrix values must be arrays. Pydantic already serializes
    tuple-based config values to lists, so scalar values are wrapped in a
    single-element list here.
    """

    allowed_keys = set(_matrix_keys(config))
    requested_keys = tuple(keys)
    for key in requested_keys:
        if key not in allowed_keys:
            raise KeyError(key)

    matrix = config.model_dump(mode="json", include=set(requested_keys))
    for key, value in matrix.items():
        if not isinstance(value, list):
            matrix[key] = [value]
    return matrix


def _print_deprecated_matrix(
    session: Session,
    config: BaseConfig,
    key_map: dict[str, str],
    session_name: str,
    replacement_args: str,
) -> None:
    matrix = _dump_matrix(config, key_map.values())
    renamed_matrix: dict[str, Any] = {}
    for output_key, config_key in key_map.items():
        renamed_matrix[output_key] = matrix[config_key]
    print(json.dumps(renamed_matrix))

    session.warn(
        f"Warning: `nox -s {session_name}` is deprecated and will be removed on "
        f"{MATRIX_DEPRECATION_DATE}. Use `nox -s matrix:generate -- {replacement_args}` "
        "instead."
    )


@nox.session(name="matrix:generate", python=False)
def generate_matrix(session: Session) -> None:
    """Output selected BaseConfig values as JSON."""
    keys = _matrix_args(session, PROJECT_CONFIG)
    matrix = _dump_matrix(PROJECT_CONFIG, keys)
    print(json.dumps(matrix))


@nox.session(name="matrix:python", python=False)
def python_matrix(session: Session) -> None:
    """Output the build matrix for Python versions as JSON."""
    _print_deprecated_matrix(
        session=session,
        config=PROJECT_CONFIG,
        key_map={"python-version": "python_versions"},
        session_name="matrix:python",
        replacement_args="python_versions",
    )


@nox.session(name="matrix:exasol", python=False)
def exasol_matrix(session: Session) -> None:
    """Output the build matrix for Exasol versions as JSON."""
    _print_deprecated_matrix(
        session=session,
        config=PROJECT_CONFIG,
        key_map={"exasol-version": "exasol_versions"},
        session_name="matrix:exasol",
        replacement_args="exasol_versions",
    )


@nox.session(name="matrix:all", python=False)
def full_matrix(session: Session) -> None:
    """Output the full build matrix for Python & Exasol versions as JSON."""
    _print_deprecated_matrix(
        session=session,
        config=PROJECT_CONFIG,
        key_map={
            "python-version": "python_versions",
            "exasol-version": "exasol_versions",
        },
        session_name="matrix:all",
        replacement_args="python_versions exasol_versions",
    )
