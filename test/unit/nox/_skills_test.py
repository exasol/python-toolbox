from unittest.mock import Mock

import pytest
from nox.sessions import _SessionQuit

import noxconfig
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

    with pytest.raises(_SessionQuit) as error:
        _skills.check_skills(nox_session)

    message = str(error.value)
    assert "one:\n  - bad frontmatter" in message
    assert "two:\n  - missing SKILL.md" in message


def test_install_skills_uses_project_skill_directory(
    monkeypatch, nox_session, tmp_path
):
    target_directory = tmp_path / ".agents" / "skills"
    targets = {name: target_directory / name for name in ("one", "two")}
    monkeypatch.setattr(
        noxconfig,
        "PROJECT_CONFIG",
        Mock(agent_skills_path=target_directory),
    )
    monkeypatch.setattr(
        _skills, "get_packaged_skill_names", Mock(return_value=("one", "two"))
    )
    install = Mock(side_effect=lambda name, target_directory: targets[name])
    monkeypatch.setattr(_skills, "install_skill", install)

    _skills.install_skills(nox_session)

    assert install.call_args_list == [
        (("one",), {"target_directory": target_directory}),
        (("two",), {"target_directory": target_directory}),
    ]


def test_tasks_exports_skill_tasks():
    # Import the public task module so its exported skill sessions are covered
    # in the same way users discover them through nox.
    from exasol.toolbox.nox import tasks

    assert tasks.check_skills is _skills.check_skills
    assert tasks.install_skills is _skills.install_skills
