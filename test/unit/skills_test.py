from pathlib import Path
from subprocess import run
from zipfile import ZipFile
from collections.abc import Mapping

import pytest
from ruamel.yaml import YAML

from exasol.toolbox.util.skills import (
    PTB_SKILL_NAME,
    get_skill_files,
    get_skill_path,
    get_packaged_skill_names,
    install_skill,
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


def _eval_cases_path(skill_name: str) -> Path:
    return (
        PROJECT_ROOT / "test" / "resources" / "skills" / skill_name / "eval_cases.yml"
    )


def _load_eval_cases(skill_name: str) -> dict:
    return YAML(typ="safe").load(_eval_cases_path(skill_name))


def _skills_with_eval_cases() -> list[str]:
    # Keep this data-driven so adding a packaged skill requires no test edit.
    return [
        skill_name
        for skill_name in get_packaged_skill_names()
        if _eval_cases_path(skill_name).is_file()
    ]


def _validate_eval_cases(eval_cases: object, skill_name: str) -> list[str]:
    # Eval cases are test resources, so validate their reusable schema here
    # instead of coupling production skill discovery to test-only files.
    errors: list[str] = []
    if not isinstance(eval_cases, Mapping):
        return ["evaluation cases must be a mapping"]
    if eval_cases.get("version") != 1:
        errors.append("version must be 1")
    if eval_cases.get("skill") != skill_name:
        errors.append(f"skill must be {skill_name}")

    cases = eval_cases.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["cases must be a non-empty list"]

    ids: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, Mapping):
            errors.append(f"case {index} must be a mapping")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"case {index} must have a non-empty id")
        else:
            ids.append(case_id)
        for field in ("category", "prompt"):
            value = case.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"case {index} must have a non-empty {field}")

        expected = case.get("expected")
        if not isinstance(expected, Mapping):
            errors.append(f"case {index} expected must be a mapping")
            continue
        for field in ("must_include", "must_not_include"):
            values = expected.get(field)
            if not isinstance(values, list) or not values:
                errors.append(f"case {index} {field} must be a non-empty list")
            elif not all(isinstance(value, str) and value.strip() for value in values):
                errors.append(f"case {index} {field} must contain non-empty strings")

    if len(ids) != len(set(ids)):
        errors.append("case ids must be unique")
    return errors


def test_ptb_skill_resources_are_available():
    skill_files = get_skill_files(PTB_SKILL_NAME)

    for expected in SKILL_FILES:
        assert expected in skill_files
        assert skill_files[expected].is_file()


def test_ptb_skill_can_be_installed(tmp_path):
    installed = install_skill(PTB_SKILL_NAME, tmp_path)

    assert installed == tmp_path / PTB_SKILL_NAME
    for expected in SKILL_FILES:
        assert (installed / expected).is_file()


@pytest.mark.parametrize("skill_name", get_packaged_skill_names())
def test_packaged_skills_can_be_installed(skill_name, tmp_path):
    installed = install_skill(skill_name, tmp_path)

    assert installed == tmp_path / skill_name
    assert (installed / "SKILL.md").is_file()


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


@pytest.mark.parametrize("skill_name", _skills_with_eval_cases())
def test_packaged_skill_eval_cases_are_valid(skill_name):
    eval_cases = _load_eval_cases(skill_name)

    assert _validate_eval_cases(eval_cases, skill_name) == []


def _minimal_eval_cases() -> dict:
    return {
        "version": 1,
        "skill": "example",
        "cases": [
            {
                "id": "case",
                "category": "quality",
                "prompt": "Check the API.",
                "expected": {
                    "must_include": ["finding"],
                    "must_not_include": ["fix"],
                },
            }
        ],
    }


@pytest.mark.parametrize(
    ("change", "expected_error"),
    [
        (lambda data: data.update(version=2), "version must be 1"),
        (
            lambda data: data.update(skill="other"),
            "skill must be example",
        ),
        (
            lambda data: data["cases"].clear(),
            "cases must be a non-empty list",
        ),
        (
            lambda data: data["cases"].append(data["cases"][0].copy()),
            "case ids must be unique",
        ),
        (
            lambda data: data["cases"][0].update(category=""),
            "case 0 must have a non-empty category",
        ),
        (
            lambda data: data["cases"][0].update(prompt=""),
            "case 0 must have a non-empty prompt",
        ),
        (
            lambda data: data["cases"][0].update(expected=None),
            "case 0 expected must be a mapping",
        ),
        (
            lambda data: data["cases"][0]["expected"].update(must_include=[]),
            "case 0 must_include must be a non-empty list",
        ),
        (
            lambda data: data["cases"][0]["expected"].update(must_not_include=[""]),
            "case 0 must_not_include must contain non-empty strings",
        ),
    ],
)
def test_eval_case_validation_rejects_invalid_cases(change, expected_error):
    eval_cases = _minimal_eval_cases()
    # Each mutation represents a malformed future eval_cases.yml file.
    change(eval_cases)

    assert expected_error in _validate_eval_cases(eval_cases, "example")


def test_ptb_skill_eval_cases_cover_ticket_scope():
    eval_cases = _load_eval_cases(PTB_SKILL_NAME)
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
    content = _eval_cases_path(PTB_SKILL_NAME).read_text(encoding="utf-8").lower()

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
