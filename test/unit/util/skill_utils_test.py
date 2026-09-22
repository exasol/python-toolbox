import pytest

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


def test_get_packaged_skill_names_reports_missing_resources(monkeypatch):
    def raise_file_not_found(_):
        raise FileNotFoundError("skills")

    monkeypatch.setattr(skills.resources, "files", raise_file_not_found)

    with pytest.raises(RuntimeError, match="Packaged PTB skills are unavailable"):
        skills.get_packaged_skill_names()


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


def test_install_skill_copies_all_files_and_replaces_previous_copy(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    skill_file = source / "SKILL.md"
    reference = source / "references" / "guide.md"
    reference.parent.mkdir()
    skill_file.write_text("new", encoding="utf-8")
    reference.write_text("guide", encoding="utf-8")
    monkeypatch.setattr(
        skills,
        "get_skill_files",
        lambda _: {"SKILL.md": skill_file, "references/guide.md": reference},
    )
    target_directory = tmp_path / ".agents" / "skills"
    previous = target_directory / "example"
    previous.mkdir(parents=True)
    (previous / "stale.md").write_text("stale", encoding="utf-8")

    installed = skills.install_skill("example", target_directory)

    assert installed == previous
    assert (installed / "SKILL.md").read_text(encoding="utf-8") == "new"
    assert (installed / "references" / "guide.md").read_text(encoding="utf-8") == "guide"
    assert not (installed / "stale.md").exists()


def test_install_skill_rejects_path_traversal(tmp_path):
    with pytest.raises(ValueError, match="invalid skill name"):
        skills.install_skill("../outside", tmp_path)


def test_install_skill_rejects_symlink_target(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    skill_file = source / "SKILL.md"
    skill_file.write_text("skill", encoding="utf-8")
    monkeypatch.setattr(skills, "get_skill_files", lambda _: {"SKILL.md": skill_file})
    target_directory = tmp_path / ".agents" / "skills"
    target_directory.mkdir(parents=True)
    target = tmp_path / "elsewhere"
    target.mkdir()
    (target_directory / "example").symlink_to(target, target_is_directory=True)

    with pytest.raises(ValueError, match="refusing to replace symlink"):
        skills.install_skill("example", target_directory)
