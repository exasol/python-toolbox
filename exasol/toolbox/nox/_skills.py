"""Nox sessions for validating packaged agent skills."""

from __future__ import annotations

import nox
from nox import Session

from exasol.toolbox.util.skills import get_packaged_skill_names, validate_skill


@nox.session(name="skills:check", python=False)
def check_skills(session: Session) -> None:
    """Validate the common structure and content rules for packaged skills."""
    failures = {
        skill_name: validate_skill(skill_name)
        for skill_name in get_packaged_skill_names()
    }
    failures = {
        skill_name: errors for skill_name, errors in failures.items() if errors
    }
    if failures:
        details = "\n".join(
            f"{skill_name}:\n" + "\n".join(f"  - {error}" for error in errors)
            for skill_name, errors in failures.items()
        )
        session.error(f"Packaged skill validation failed:\n{details}")
