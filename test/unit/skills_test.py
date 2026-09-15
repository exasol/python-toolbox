from pathlib import Path
from subprocess import run
from zipfile import ZipFile

from ruamel.yaml import YAML

from exasol.toolbox.util.skills import (
    PTB_SKILL_NAME,
    get_skill_files,
    get_skill_path,
    validate_skill,
)

PROJECT_ROOT = Path(__file__).parents[2]
SKILL = get_skill_path(PTB_SKILL_NAME)
SKILL_FILES = [
    "SKILL.md",
    "references/coding-guidelines.md",
    "references/common-workflows.md",
    "references/nox-sessions.md",
    "references/source-routing.md",
]
EVAL_CASES = (
    PROJECT_ROOT
    / "test"
    / "resources"
    / "skills"
    / "exasol-python-toolbox"
    / "eval_cases.yml"
)


def _load_eval_cases() -> dict:
    return YAML(typ="safe").load(EVAL_CASES)


def test_ptb_skill_resources_are_available():
    skill_files = get_skill_files(PTB_SKILL_NAME)

    for expected in SKILL_FILES:
        assert expected in skill_files
        assert skill_files[expected].is_file()


def test_ptb_skill_resources_are_packaged(tmp_path):
    build_output = tmp_path / "dist"
    result = run(
        [
            "poetry",
            "build",
            "--project",
            str(PROJECT_ROOT),
            "--format",
            "wheel",
            "--output",
            str(build_output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    wheels = list(build_output.glob("*.whl"))
    assert len(wheels) == 1

    with ZipFile(wheels[0]) as wheel:
        wheel_files = set(wheel.namelist())

    expected_files = {
        f"exasol/toolbox/skills/{PTB_SKILL_NAME}/{path}" for path in SKILL_FILES
    }
    assert expected_files <= wheel_files


def test_ptb_skill_frontmatter_is_complete():
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = content.split("---", maxsplit=2)[1]

    assert "name: exasol-python-toolbox" in frontmatter
    assert "description: Use this skill in Exasol Python projects" in frontmatter
    assert "[TODO" not in content


def test_ptb_skill_passes_shared_validation():
    assert validate_skill(PTB_SKILL_NAME) == ()


def test_ptb_skill_eval_cases_are_valid():
    eval_cases = _load_eval_cases()

    assert eval_cases["version"] == 1
    assert eval_cases["skill"] == "exasol-python-toolbox"
    # Keep enough cases to cover the ticket scope, but not so many that the
    # deterministic eval file becomes hard to review.
    assert 6 <= len(eval_cases["cases"]) <= 8

    ids = [case["id"] for case in eval_cases["cases"]]
    assert len(ids) == len(set(ids))

    for case in eval_cases["cases"]:
        assert case["id"]
        assert case["category"]
        assert case["prompt"]
        assert case["expected"]["must_include"]
        assert case["expected"]["must_not_include"]


def test_ptb_skill_eval_cases_cover_ticket_scope():
    eval_cases = _load_eval_cases()
    categories = {case["category"] for case in eval_cases["cases"]}

    assert {
        "setup",
        "quality",
        "release",
        "update",
        "workflow",
        "source-routing",
    }.issubset(categories)


def test_ptb_skill_eval_cases_do_not_define_llm_ci_execution():
    content = EVAL_CASES.read_text(encoding="utf-8").lower()

    forbidden = [
        "model:",
        "api_key",
        "openai",
        "chatgpt",
        "codex",
        "temperature",
    ]

    for term in forbidden:
        assert term not in content
