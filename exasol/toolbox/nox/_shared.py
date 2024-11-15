from __future__ import annotations

import argparse
from enum import (
    Enum,
    auto,
)
from pathlib import Path
from typing import (
    Any,
    ChainMap,
    Iterable,
    MutableMapping,
)

from nox import Session

from noxconfig import PROJECT_CONFIG

DOCS_OUTPUT_DIR = ".html-documentation"


class Mode(Enum):
    Fix = auto()
    Check = auto()


def python_files(project_root: Path) -> Iterable[Path]:
    path_filters = tuple(["dist", ".eggs", "venv"] + list(PROJECT_CONFIG.path_filters))
    return _python_files(project_root, path_filters)


def _python_files(
    project_root: Path, path_filters: Iterable[str] = ("dist", ".eggs", "venv")
) -> Iterable[Path]:
    """Returns all relevant"""
    return _deny_filter(project_root.glob("**/*.py"), deny_list=path_filters)


def _deny_filter(files: Iterable[Path], deny_list: Iterable[str]) -> Iterable[Path]:
    """
    Adds a filter to remove unwanted paths containing python files from the iterator.
    """
    for entry in deny_list:
        files = list(filter(lambda path: entry not in path.parts, files))
    return files


def _version(session: Session, mode: Mode, version_file: Path) -> None:
    command = ["poetry", "run", "version-check"]
    command = command if mode == Mode.Check else command + ["--fix"]
    session.run(*command, f"{version_file}")


def _context_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--db-version")
    parser.add_argument("--coverage", action="store_true")
    return parser


def _context(session: Session, **kwargs: Any) -> MutableMapping[str, Any]:
    parser = _context_parser()
    namespace, args = parser.parse_known_args(session.posargs)
    cli_context: MutableMapping[str, Any] = vars(namespace)
    cli_context["fwd-args"] = args
    default_context = {"db_version": "7.1.9", "coverage": False}
    # Note: ChainMap scans last to first
    return ChainMap(kwargs, cli_context, default_context)
