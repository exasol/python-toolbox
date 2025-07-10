import subprocess


def test_poetry_check_passes(new_project):
    """
    If this tests fails, this indicates that the `pyproject.toml` is not compatible
    with the PTB's default poetry version. Note, that this checks only known poetry
    attributes, so there could be keys, like `project-abc = 127`, that are present, but,
    as they do not have a meaning for poetry, they are ignored.
    """
    output = subprocess.run(["poetry", "check"], cwd=new_project,
                            capture_output=True, text=True)

    assert output.stderr == ""
    assert output.stdout == "All set!\n"
