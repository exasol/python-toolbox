from pathlib import Path
from subprocess import run
from zipfile import ZipFile

import pytest
from ruamel.yaml import YAML

from exasol.toolbox.util.skill_eval import PackagedSkillEvalCases
from exasol.toolbox.util.skills import (
    PTB_SKILL_NAME,
    get_packaged_skill_names,
    get_skill_files,
    get_skill_path,
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
class TestPackagedSkillEvalCases:
    @pytest.fixture(scope="module")
    def eval_cases_by_skill(self):
        # Parse each packaged artifact once so all checks use the same model.
        return {
            skill_name: PackagedSkillEvalCases.model_validate(
                _load_eval_cases(skill_name)
            )
            for skill_name in _skills_with_eval_cases()
        }

    @pytest.fixture
    def eval_cases(self, eval_cases_by_skill, skill_name):
        return eval_cases_by_skill[skill_name]

    def test_has_expected_metadata(self, eval_cases, skill_name):
        assert eval_cases.version == 1
        assert eval_cases.skill == skill_name
        assert eval_cases.cases

    def test_cases_have_required_fields(self, eval_cases):
        for case in eval_cases.cases:
            assert case.id
            assert case.category
            assert case.prompt

    def test_cases_have_response_constraints(self, eval_cases):
        for case in eval_cases.cases:
            assert case.expected.must_include
            assert case.expected.must_not_include
            assert all(value.strip() for value in case.expected.must_include)
            assert all(value.strip() for value in case.expected.must_not_include)

    def test_case_ids_are_unique(self, eval_cases):
        ids = [case.id for case in eval_cases.cases]

        assert len(ids) == len(set(ids))


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
