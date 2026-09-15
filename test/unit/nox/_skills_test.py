from unittest.mock import Mock

import pytest
from nox.sessions import _SessionQuit

from exasol.toolbox.nox import _skills


def test_check_skills_passes_when_all_skills_are_valid(monkeypatch, nox_session):
    monkeypatch.setattr(
        _skills, "get_packaged_skill_names", Mock(return_value=("one",))
    )
    validate = Mock(return_value=())
    monkeypatch.setattr(_skills, "validate_skill", validate)

    _skills.check_skills(nox_session)

    validate.assert_called_once_with("one")


def test_check_skills_reports_all_failures(monkeypatch, nox_session):
    monkeypatch.setattr(
        _skills,
        "get_packaged_skill_names",
        Mock(return_value=("one", "two")),
    )
    monkeypatch.setattr(
        _skills,
        "validate_skill",
        Mock(side_effect=(("bad frontmatter",), ("missing SKILL.md",))),
    )

    with pytest.raises(_SessionQuit, match="Packaged skill validation failed"):
        _skills.check_skills(nox_session)
