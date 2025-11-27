import json
from inspect import cleandoc
from pathlib import Path
from unittest.mock import patch

import pytest
from nox.command import CommandFailed

from exasol.toolbox.nox._lint import (
    lint,
    security_lint,
    type_check,
)


@pytest.fixture
def file_with_multiple_problems(tmp_path):
    """
    In this file with multiple problems, it is expected that the nox
    lint sessions would detect the following errors:

    * lint:code
       * C0304: Final newline missing (missing-final-newline)
       * C0114: Missing module docstring (missing-module-docstring)
       * W1510: 'subprocess.run' used without explicitly defining the value for 'check'. (subprocess-run-check)
    * lint:typing
       * Incompatible types in assignment (expression has type "int", variable has type "str")  [assignment]
    * lint:security
        * [B404:blacklist] Consider possible security implications associated with the subprocess module.
        * [B607:start_process_with_partial_path] Starting a process with a partial executable path
        * [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
    """

    file_path = tmp_path / "dummy_file.py"
    text = """
    import subprocess

    x: str = 2
    subprocess.run("ls")
    """
    file_path.write_text(cleandoc(text))
    return file_path


def test_lint(nox_session, tmp_path, file_with_multiple_problems):
    with patch("exasol.toolbox.nox._lint.PROJECT_CONFIG") as config:
        config.root = tmp_path
        config.source = Path("")
        with pytest.raises(CommandFailed, match="Returned code 20"):
            lint(session=nox_session)

    json_file = tmp_path / ".lint.json"
    txt_file = tmp_path / ".lint.txt"

    assert json_file.exists()
    assert txt_file.exists()

    contents = json_file.read_text()
    errors = {row["message-id"] for row in json.loads(contents)}
    assert {"C0114", "C0304", "W1510"}.issubset(errors)


def test_type_check(nox_session, tmp_path, file_with_multiple_problems, caplog):
    with patch("exasol.toolbox.nox._lint.PROJECT_CONFIG") as config:
        config.root = tmp_path
        config.source = Path("")
        with pytest.raises(CommandFailed, match="Returned code 1"):
            type_check(session=nox_session)

    assert caplog.messages[1] == (
        "Command mypy --explicit-package-bases --namespace-packages --show-error-codes "
        "--pretty --show-column-numbers --show-error-context --scripts-are-modules "
        f"{file_with_multiple_problems} failed with exit code 1"
    )


def test_security_lint(nox_session, tmp_path, file_with_multiple_problems):
    with patch("exasol.toolbox.nox._lint.PROJECT_CONFIG") as config:
        config.root = tmp_path
        config.source = Path("")
        security_lint(session=nox_session)

    output_file = tmp_path / ".security.json"
    assert output_file.exists()

    contents = output_file.read_text()
    assert json.loads(contents)["metrics"]["_totals"] == {
        "CONFIDENCE.HIGH": 3,
        "CONFIDENCE.LOW": 0,
        "CONFIDENCE.MEDIUM": 0,
        "CONFIDENCE.UNDEFINED": 0,
        "SEVERITY.HIGH": 0,
        "SEVERITY.LOW": 3,
        "SEVERITY.MEDIUM": 0,
        "SEVERITY.UNDEFINED": 0,
        "loc": 3,
        "nosec": 0,
        "skipped_tests": 0,
    }
