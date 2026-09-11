"""Utilities for validating packaged agent skills."""

from collections.abc import Mapping
from pathlib import Path
from typing import Final

import importlib_resources as resources

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


def get_skill_path(skill_name: str = PTB_SKILL_NAME) -> Path:
    """
    Return the path to a packaged skill.
    """
    return Path(str(resources.files(SKILLS_DIRECTORY) / skill_name))


def get_skill_files(skill_name: str = PTB_SKILL_NAME) -> Mapping[str, Path]:
    """
    Return packaged skill files.

    The keys are paths relative to the skill root.
    """
    skill_path = get_skill_path(skill_name)
    return {
        str(path.relative_to(skill_path)): path
        for path in skill_path.rglob("*")
        if path.is_file()
    }


def get_packaged_skill_names() -> tuple[str, ...]:
    """Return the names of all skills packaged with the toolbox."""
    skills_path = Path(str(resources.files(SKILLS_DIRECTORY)))
    return tuple(sorted(path.name for path in skills_path.iterdir() if path.is_dir()))


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

    skill_file = skill_files.get("SKILL.md")
    if skill_file is None:
        return tuple(errors)

    content = skill_file.read_text(encoding="utf-8")
    parts = content.split(SKILL_FRONTMATTER_SEPARATOR, maxsplit=2)
    if len(parts) != 3 or parts[0].strip():
        errors.append("SKILL.md must start with YAML frontmatter")
    else:
        frontmatter = parts[1]
        if f"name: {skill_name}" not in frontmatter:
            errors.append(f"frontmatter name must be {skill_name}")
        if "description:" not in frontmatter:
            errors.append("frontmatter must contain a description")

    if "[TODO" in content:
        errors.append("contains a TODO marker")

    all_content = "\n".join(
        path.read_text(encoding="utf-8")
        for path in skill_files.values()
    ).lower()
    for term in SKILL_FORBIDDEN_TERMS:
        if term in all_content:
            errors.append(f"contains forbidden term: {term}")

    nox_reference = "references/nox-sessions.md"
    for relative_path, path in skill_files.items():
        if not relative_path.endswith(".md"):
            continue
        seen: dict[str, int] = {}
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            normalized = line.strip().lower()
            if (
                not normalized
                or normalized in {"---", "```bash", "```"}
                or normalized.startswith("|")
            ):
                continue
            if normalized in seen:
                errors.append(
                    f"{relative_path} duplicates line {seen[normalized]} "
                    f"at line {line_number}"
                )
            seen[normalized] = line_number

        if relative_path != nox_reference:
            text = path.read_text(encoding="utf-8")
            if "poetry run -- nox -s" in text or "poetry run -- nox -l" in text:
                errors.append(
                    f"{relative_path} contains Nox command syntax outside "
                    f"{nox_reference}"
                )

    return tuple(errors)
