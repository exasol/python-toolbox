from __future__ import annotations

import argparse
from collections import ChainMap
from collections.abc import (
    MutableMapping,
)
from enum import (
    Enum,
    auto,
)
from pathlib import Path
from typing import Any

from nox import Session

from noxconfig import (
    PROJECT_CONFIG,
)

DOCS_OUTPUT_DIR = ".html-documentation"


class Mode(Enum):
    Fix = auto()
    Check = auto()


def get_filtered_python_files(project_root: Path) -> list[str]:
    """
    Returns iterable of Python files after removing excluded paths
    """
    files = project_root.glob("**/*.py")

    def exclude(path: Path):
        current = set(path.parents) | {path}
        return current.intersection(PROJECT_CONFIG.excluded_python_paths)

    return [f"{path}" for path in files if not exclude(path)]


def _context_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    return parser


def _context(
    session: Session,
    parser: argparse.ArgumentParser,
    default_context: dict[str, Any],
    **kwargs: Any,
) -> MutableMapping[str, Any]:
    namespace, args = parser.parse_known_args(session.posargs)
    cli_context: MutableMapping[str, Any] = vars(namespace)
    cli_context["fwd-args"] = args
    # Note: ChainMap scans last to first
    return ChainMap(kwargs, cli_context, default_context)


def _unit_test_context(session: Session, **kwargs: Any) -> MutableMapping[str, Any]:
    parser = _context_parser()
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    return _context(session, parser, {"coverage": False}, **kwargs)


def _integration_test_context(
    session: Session,
    **kwargs: Any,
) -> MutableMapping[str, Any]:
    parser = _context_parser()
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    parser.add_argument(
        "--db-version",
        default=PROJECT_CONFIG.minimum_exasol_version,
        help="Specify the Exasol DB version to be used",
    )
    return _context(
        session,
        parser,
        {
            "coverage": False,
            "db_version": PROJECT_CONFIG.minimum_exasol_version,
        },
        **kwargs,
    )
