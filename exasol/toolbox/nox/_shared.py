from __future__ import annotations

from enum import (
    Enum,
    auto,
)
from pathlib import Path

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
