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


def _matrix_keys(config: BaseConfig) -> tuple[str, ...]:
    """
    Return the config keys that can be selected for matrix generation.

    Pydantic stores explicitly declared config attributes in ``model_fields``
    and derived ``@computed_field`` values in ``model_computed_fields``. We
    include both because matrix inputs may come from either source: a declared
    field such as ``extra_matrix_value`` or a computed value such as
    ``computed_matrix_value``.
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


def _generate_matrix(config: BaseConfig, keys: Iterable[str]) -> dict[str, Any]:
    """
    Generate a JSON-serializable matrix subset from the project's config.

    The selected keys may refer to either declared fields or computed fields.
    GitHub Actions matrix values must be arrays. Pydantic already serializes
    tuple-based config values to lists, so scalar values are wrapped in a
    single-element list here.
    """
    matrix = config.model_dump(mode="json", include=set(keys))
    return {
        key: value if isinstance(value, list) else [value]
        for key, value in matrix.items()
    }


@nox.session(name="matrix:generate", python=False)
def generate_matrix(session: Session) -> None:
    """Output selected BaseConfig values as JSON."""
    keys = _matrix_args(session, PROJECT_CONFIG)
    matrix = _generate_matrix(PROJECT_CONFIG, keys)
    print(json.dumps(matrix))
