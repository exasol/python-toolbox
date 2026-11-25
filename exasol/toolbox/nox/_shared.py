from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import (
    Enum,
    auto,
)
from pathlib import Path

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


def validate_path_within_root(path: Path) -> Path:
    """
    Resolve a path and ensure its parent directory stays inside the project root.
    """
    resolved_path = path.resolve(strict=False)
    resolved_root = PROJECT_CONFIG.root_path.resolve(strict=False)

    if not resolved_path.parent.is_relative_to(resolved_root):
        raise ValueError(
            f"path must be located inside the project root: {resolved_root}. "
            f"Got: {resolved_path}"
        )

    return resolved_path


@dataclass
class ArgparseResults:
    known: argparse.Namespace
    other: list[str]


def _unit_test_context(session: Session) -> ArgparseResults:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    default_path = PROJECT_CONFIG.root_path / "test" / "unit"
    parser.add_argument("directories", nargs="*", type=Path, default=[default_path])
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    return ArgparseResults(*parser.parse_known_args(session.posargs))


def _integration_test_context(session: Session) -> ArgparseResults:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    default_path = PROJECT_CONFIG.root_path / "test" / "integration"
    parser.add_argument("directories", nargs="*", type=Path, default=[default_path])
    parser.add_argument(
        "--coverage", action="store_true", help="Enable the collection of coverage data"
    )
    parser.add_argument(
        "--db-version",
        default=PROJECT_CONFIG.minimum_exasol_version,
        help="Specify the Exasol DB version to be used",
    )
    return ArgparseResults(*parser.parse_known_args(session.posargs))
