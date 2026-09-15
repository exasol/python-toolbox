"""Utilities for validating packaged agent skills."""

from collections.abc import Mapping
from pathlib import Path
import shutil
from typing import Final

import importlib_resources as resources
from importlib_resources.abc import Traversable

SKILLS_DIRECTORY: Final = "exasol.toolbox.skills"
PTB_SKILL_NAME: Final = "exasol-python-toolbox"
SKILL_FRONTMATTER_SEPARATOR: Final = "---"
SKILL_FORBIDDEN_TERMS: Final = (
    "main-branch",
    "main branch",
    "master-branch",
    "master branch",
    "inventory",
    "source-map",
)
SKILL_FILES: Final = ("SKILL.md",)


def get_skill_path(skill_name: str = PTB_SKILL_NAME) -> Traversable:
    """
    Return the path to a packaged skill.
    """
    return resources.files(SKILLS_DIRECTORY) / skill_name


def _find_files(
    root: Traversable, relative_directory: str = ""
) -> dict[str, Traversable]:
    """Return all files below a package resource directory."""
    files: dict[str, Traversable] = {}
    for child in root.iterdir():
        relative_path = f"{relative_directory}{child.name}"
        if child.is_file():
            files[relative_path] = child
        elif child.is_dir():
            files.update(_find_files(child, f"{relative_path}/"))
    return files


def get_skill_files(skill_name: str = PTB_SKILL_NAME) -> Mapping[str, Traversable]:
    """
    Return packaged skill files.

    The keys are paths relative to the skill root.
    """
    return _find_files(get_skill_path(skill_name))


def get_packaged_skill_names() -> tuple[str, ...]:
    """Return the names of all skills packaged with the toolbox."""
    return tuple(
        sorted(
            path.name
            for path in resources.files(SKILLS_DIRECTORY).iterdir()
            if path.is_dir()
        )
    )


def _has_symlink_in_parents(path: Path) -> bool:
    """Return whether a path or one of its existing parents is a symlink."""
    return any(candidate.is_symlink() for candidate in (path, *path.parents))


def install_skill(
    skill_name: str = PTB_SKILL_NAME,
    target_directory: Path | None = None,
) -> Path:
    """Install a packaged skill into a project-local agent skill directory."""
    if Path(skill_name).name != skill_name:
        raise ValueError(f"invalid skill name: {skill_name}")

    source_files = get_skill_files(skill_name)
    if not source_files:
        raise ValueError(f"packaged skill does not exist: {skill_name}")

    target_directory = target_directory or Path.cwd() / ".agents" / "skills"
    target_skill = target_directory / skill_name
    if _has_symlink_in_parents(target_directory):
        raise ValueError(f"refusing to use symlinked target directory: {target_directory}")
    if target_skill.is_symlink():
        raise ValueError(f"refusing to replace symlink: {target_skill}")
    if target_skill.exists() and not target_skill.is_dir():
        raise ValueError(f"skill target is not a directory: {target_skill}")

    if target_skill.exists():
        shutil.rmtree(target_skill)
    target_skill.mkdir(parents=True, exist_ok=True)
    for relative_path, source in source_files.items():
        destination = target_skill / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    return target_skill


def _validate_frontmatter(content: str, skill_name: str) -> list[str]:
    """Validate the frontmatter of a skill description."""
    parts = content.split(SKILL_FRONTMATTER_SEPARATOR, maxsplit=2)
    if len(parts) != 3 or parts[0].strip():
        return ["SKILL.md must start with YAML frontmatter"]

    errors = []
    frontmatter = parts[1]
    if f"name: {skill_name}" not in frontmatter:
        errors.append(f"frontmatter name must be {skill_name}")
    if "description:" not in frontmatter:
        errors.append("frontmatter must contain a description")
    return errors


def _validate_markdown_file(relative_path: str, content: str) -> list[str]:
    """Validate shared rules for one Markdown file."""
    errors: list[str] = []
    seen: dict[str, int] = {}
    ignored_lines = {"---", "```bash", "```"}
    for line_number, line in enumerate(content.splitlines(), 1):
        normalized = line.strip().lower()
        if not normalized or normalized in ignored_lines or normalized.startswith("|"):
            continue
        if normalized in seen:
            errors.append(
                f"{relative_path} duplicates line {seen[normalized]} "
                f"at line {line_number}"
            )
        seen[normalized] = line_number
    return errors


def _validate_nox_syntax(relative_path: str, content: str) -> list[str]:
    """Ensure Nox command syntax is kept in the dedicated reference."""
    nox_reference = "references/nox-sessions.md"
    if relative_path != nox_reference and any(
        command in content
        for command in ("poetry run -- nox -s", "poetry run -- nox -l")
    ):
        return [f"{relative_path} contains Nox command syntax outside {nox_reference}"]
    return []


def validate_skill(skill_name: str) -> tuple[str, ...]:
    """Return deterministic validation errors for a packaged skill.

    The checks here are deliberately limited to properties shared by every PTB
    skill.  Assertions about a skill's specific content belong in that skill's
    own tests.
    """
    skill_files = get_skill_files(skill_name)
    errors: list[str] = []

    for expected_file in SKILL_FILES:
        if expected_file not in skill_files:
            errors.append(f"missing required file: {expected_file}")

    skill_content = skill_files.get("SKILL.md")
    if skill_content is None:
        return tuple(errors)

    content = skill_content.read_text(encoding="utf-8")
    errors.extend(_validate_frontmatter(content, skill_name))

    if "[TODO" in content:
        errors.append("contains a TODO marker")

    all_content = "\n".join(
        path.read_text(encoding="utf-8") for path in skill_files.values()
    ).lower()
    for term in SKILL_FORBIDDEN_TERMS:
        if term in all_content:
            errors.append(f"contains forbidden term: {term}")

    for relative_path, path in skill_files.items():
        if not relative_path.endswith(".md"):
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(_validate_markdown_file(relative_path, text))
        errors.extend(_validate_nox_syntax(relative_path, text))

    return tuple(errors)
