from unittest.mock import Mock

import noxconfig

from exasol.toolbox.nox import _skills
from exasol.toolbox.util.skills import get_packaged_skill_names


def test_skills_check_validates_all_packaged_skills():
    # Use real package resources here; unit tests separately cover failure
    # formatting with mocked skill names and validation results.
    packaged_skills = get_packaged_skill_names()

    assert {"api-contract-audit", "exasol-python-toolbox"}.issubset(packaged_skills)

    session = Mock()
    _skills.check_skills(session)

    session.error.assert_not_called()


def test_skills_install_installs_all_packaged_skills(tmp_path, monkeypatch):
    monkeypatch.setattr(noxconfig, "PROJECT_CONFIG", Mock(agent_skills_path=tmp_path))

    _skills.install_skills(Mock())

    for skill_name in get_packaged_skill_names():
        assert (tmp_path / skill_name / "SKILL.md").is_file()
