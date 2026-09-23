"""Nox sessions for validating packaged agent skills."""

from __future__ import annotations

import nox
from nox import Session

from exasol.toolbox.util.skills import (
    get_packaged_skill_names,
    install_skill,
    validate_skill,
)


def _format_skill_errors(skill_name: str, errors: tuple[str, ...]) -> str:
    """Format validation errors for one skill."""
    error_list = "\n".join(f"  - {error}" for error in errors)
    return f"{skill_name}:\n{error_list}"


@nox.session(name="skills:check", python=False)
def check_skills(session: Session) -> None:
    """Validate the common structure and content rules for packaged skills."""
    failures = {}
    for skill_name in get_packaged_skill_names():
        errors = validate_skill(skill_name)
        if errors:
            failures[skill_name] = errors
    if failures:
        details = "\n".join(
            _format_skill_errors(skill_name, errors)
            for skill_name, errors in failures.items()
        )
        session.error(f"Packaged skill validation failed:\n{details}")


@nox.session(name="skills:install", python=False)
def install_ptb_skill(session: Session) -> None:
    """Install the PTB skill into the project's local agent skill directory."""
    from noxconfig import PROJECT_CONFIG

    target = install_skill(target_directory=PROJECT_CONFIG.agent_skills_path)
    session.log(f"Installed {target.name} skill to {target}")
