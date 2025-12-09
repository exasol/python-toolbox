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

from exasol.toolbox.config import BaseConfig
from noxconfig import (
    PROJECT_CONFIG,
)

DOCS_OUTPUT_DIR = ".html-documentation"


def check_for_config_attribute(config: BaseConfig, attribute: str):
    if not hasattr(config, attribute):
        raise AttributeError(
            "in the noxconfig.py file, the class Config should inherit "
            "from `exasol.toolbox.config.BaseConfig`. This is used to "
            f"set the default `{attribute}`. If the allowed "
            f"`{attribute} needs to differ in your project and is an "
            "input parameter (not property), you can set it in the PROJECT_CONFIG statement."
        )


class Mode(Enum):
    Fix = auto()
    Check = auto()


def get_filtered_python_files(project_root: Path) -> list[str]:
    """
    Returns iterable of Python files after removing excluded paths
    """
    check_for_config_attribute(config=PROJECT_CONFIG, attribute="excluded_python_paths")
    files = project_root.glob("**/*.py")
    return [
        f"{path}"
        for path in files
        if not set(path.parts).intersection(PROJECT_CONFIG.excluded_python_paths)
    ]


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
