from __future__ import annotations

import argparse
from collections import ChainMap
from collections.abc import (
    Iterable,
    MutableMapping,
)
from enum import (
    Enum,
    auto,
)
from pathlib import Path
from typing import Any

from nox import Session

from noxconfig import PROJECT_CONFIG

DEFAULT_PATH_FILTERS = {"dist", ".eggs", "venv", ".poetry"}
DOCS_OUTPUT_DIR = ".html-documentation"

MINIMUM_PYTHON_VERSION = "3.9"


class Mode(Enum):
    Fix = auto()
    Check = auto()


def python_files(project_root: Path) -> Iterable[str]:
    """
    Returns iterable of python files after removing unwanted paths
    """
    deny_list = DEFAULT_PATH_FILTERS.union(set(PROJECT_CONFIG.path_filters))

    files = project_root.glob("**/*.py")
    return [f"{path}" for path in files if not set(path.parts).intersection(deny_list)]


def _version(session: Session, mode: Mode) -> None:
    command = ["nox", "-s", "version:check", "--"]
    command = command if mode == Mode.Check else command + ["--fix"]
    session.run(*command)


def _context_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--db-version", default="7.1.9", help="Specify the Exasol DB version to be used"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    return parser


def _context(session: Session, **kwargs: Any) -> MutableMapping[str, Any]:
    parser = _context_parser()
    namespace, args = parser.parse_known_args(session.posargs)
    cli_context: MutableMapping[str, Any] = vars(namespace)
    cli_context["fwd-args"] = args
    default_context = {"db_version": "7.1.9", "coverage": False}
    # Note: ChainMap scans last to first
    return ChainMap(kwargs, cli_context, default_context)
