from ast import literal_eval
from pathlib import Path
from subprocess import run
from zipfile import ZipFile

PROJECT_ROOT = Path(__file__).parents[2]
SKILL = PROJECT_ROOT / "exasol" / "toolbox" / "skills" / "exasol-python-toolbox"
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


def _parse_quoted_value(value: str) -> str:
    return literal_eval(value.strip())


def _load_eval_cases_without_yaml_parser() -> dict:
    result: dict = {"cases": []}
    current_case: dict | None = None
    current_list: list[str] | None = None

    for raw_line in EVAL_CASES.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("version:"):
            result["version"] = int(stripped.split(":", maxsplit=1)[1].strip())
            continue
        if stripped.startswith("skill:"):
            result["skill"] = _parse_quoted_value(stripped.split(":", maxsplit=1)[1])
            continue
        if stripped == "cases:":
            continue
        if stripped.startswith("- id:"):
            current_case = {"expected": {"must_include": [], "must_not_include": []}}
            result["cases"].append(current_case)
            current_case["id"] = _parse_quoted_value(stripped.split(":", maxsplit=1)[1])
            current_list = None
            continue
        if current_case is None:
            continue
        if stripped.startswith("category:"):
            current_case["category"] = _parse_quoted_value(
                stripped.split(":", maxsplit=1)[1]
            )
            continue
        if stripped.startswith("prompt:"):
            current_case["prompt"] = _parse_quoted_value(
                stripped.split(":", maxsplit=1)[1]
            )
            continue
        if stripped == "expected:":
            continue
        if stripped == "must_include:":
            current_list = current_case["expected"]["must_include"]
            continue
        if stripped == "must_not_include:":
            current_list = current_case["expected"]["must_not_include"]
            continue
        if stripped.startswith("- "):
            assert current_list is not None
            current_list.append(_parse_quoted_value(stripped[2:]))

    return result


def _load_eval_cases() -> dict:
    try:
        from ruamel.yaml import YAML
    except ModuleNotFoundError:
        return _load_eval_cases_without_yaml_parser()

    return YAML(typ="safe").load(EVAL_CASES)


def test_ptb_skill_resources_are_available():
    for expected in SKILL_FILES:
        assert (SKILL / expected).is_file()


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
        f"exasol/toolbox/skills/exasol-python-toolbox/{path}" for path in SKILL_FILES
    }
    assert expected_files <= wheel_files


def test_ptb_skill_frontmatter_is_complete():
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = content.split("---", maxsplit=2)[1]

    assert "name: exasol-python-toolbox" in frontmatter
    assert "description: Use this skill in Exasol Python projects" in frontmatter
    assert "[TODO" not in content


def test_ptb_skill_has_no_main_branch_metadata():
    forbidden = [
        "main-branch",
        "main branch",
        "inventory",
        "source-map",
    ]
    content = "\n".join(
        path.read_text(encoding="utf-8") for path in SKILL.rglob("*") if path.is_file()
    ).lower()

    for term in forbidden:
        assert term not in content


def test_ptb_skill_has_no_duplicate_markdown_lines():
    for path in SKILL.rglob("*.md"):
        seen = {}
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            normalized = line.strip().lower()
            if (
                not normalized
                or normalized in {"---", "```bash", "```"}
                or normalized.startswith("|")
            ):
                continue
            assert normalized not in seen, (
                f"{path} duplicates line {seen[normalized]} at line {line_number}: "
                f"{line}"
            )
            seen[normalized] = line_number


def test_nox_command_syntax_is_only_in_nox_session_reference():
    nox_reference = SKILL / "references" / "nox-sessions.md"
    for path in SKILL.rglob("*"):
        if not path.is_file() or path == nox_reference:
            continue

        content = path.read_text(encoding="utf-8")
        assert "poetry run -- nox -s" not in content
        assert "poetry run -- nox -l" not in content


def test_ptb_skill_eval_cases_are_valid():
    eval_cases = _load_eval_cases()

    assert eval_cases["version"] == 1
    assert eval_cases["skill"] == "exasol-python-toolbox"
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
