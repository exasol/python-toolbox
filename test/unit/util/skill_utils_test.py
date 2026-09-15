from exasol.toolbox.util import skills


def test_validate_skill_accepts_packaged_ptb_skill():
    assert skills.validate_skill(skills.PTB_SKILL_NAME) == ()


def test_validate_skill_reports_missing_skill_file(monkeypatch):
    monkeypatch.setattr(skills, "get_skill_files", lambda _: {})

    assert skills.validate_skill("example") == ("missing required file: SKILL.md",)


def test_get_packaged_skill_names_is_sorted():
    assert skills.PTB_SKILL_NAME in skills.get_packaged_skill_names()
    assert skills.get_packaged_skill_names() == tuple(
        sorted(skills.get_packaged_skill_names())
    )
