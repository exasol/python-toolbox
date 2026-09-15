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


def test_get_skill_files_recurses_into_resource_directories(tmp_path, monkeypatch):
    reference = tmp_path / "references" / "guide.md"
    reference.parent.mkdir()
    reference.write_text("guide", encoding="utf-8")
    monkeypatch.setattr(skills, "get_skill_path", lambda _: tmp_path)

    files = skills.get_skill_files("example")

    assert set(files) == {"references/guide.md"}
    assert files["references/guide.md"].read_text(encoding="utf-8") == "guide"


def test_validate_skill_reports_shared_rule_violations(tmp_path, monkeypatch):
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text(
        """---
name: wrong
---
[TODO: finish]
main branch
main branch
poetry run -- nox -s test:unit
""",
        encoding="utf-8",
    )
    (tmp_path / "notes.txt").write_text("notes", encoding="utf-8")
    monkeypatch.setattr(skills, "get_skill_path", lambda _: tmp_path)

    errors = skills.validate_skill("example")

    assert "frontmatter name must be example" in errors
    assert "frontmatter must contain a description" in errors
    assert "contains a TODO marker" in errors
    assert "contains forbidden term: main branch" in errors
    assert "SKILL.md duplicates line 5 at line 6" in errors
    assert (
        "SKILL.md contains Nox command syntax outside references/nox-sessions.md"
        in errors
    )


def test_validate_skill_requires_frontmatter(tmp_path, monkeypatch):
    (tmp_path / "SKILL.md").write_text("skill", encoding="utf-8")
    monkeypatch.setattr(skills, "get_skill_path", lambda _: tmp_path)

    assert "SKILL.md must start with YAML frontmatter" in skills.validate_skill(
        "example"
    )
