import argparse
from enum import (
    Enum,
    auto,
)
from functools import partial
from pathlib import Path
from typing import (
    Any,
    ChainMap,
    MutableMapping,
)

from nox import Session

from exasol.toolbox.project import python_files as _python_files
from noxconfig import PROJECT_CONFIG

DOCS_OUTPUT_DIR = ".html-documentation"
PATH_FILTER = tuple(["dist", ".eggs", "venv"] + list(PROJECT_CONFIG.path_filters))

python_files = partial(_python_files, path_filters=PATH_FILTER)


class Mode(Enum):
    Fix = auto()
    Check = auto()


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
    namespace, _ = parser.parse_known_args(session.posargs)
    cli_context: MutableMapping[str, Any] = vars(namespace)
    default_context = {"db_version": "7.1.9", "coverage": False}
    # Note: ChainMap scans last to first
    return ChainMap(kwargs, cli_context, default_context)
