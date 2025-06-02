import contextlib
import re
from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path
from unittest.mock import (
    Mock,
    call,
    patch,
)

import pytest

from exasol.toolbox.nox._artifacts import copy_artifacts


@contextlib.contextmanager
def mock_session(path: Path, python_version: str, *files: str):
    with patch("exasol.toolbox.nox._artifacts.PROJECT_CONFIG") as config:
        config.python_versions = [python_version]
        for rel in files:
            file = path / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(rel)
        yield Mock(posargs=[str(path)])


def test_missing_files(tmp_path, capsys):
    with mock_session(tmp_path, "9.9") as session:
        copy_artifacts(session)
    captured = capsys.readouterr()
    assert re.match(
        cleandoc(
            f"""
            Could not find any file .*/coverage-python9.9\\*/.coverage
            File not found .*/lint-python9.9/.lint.txt
            File not found .*/lint-python9.9/.lint.json
            File not found .*/security-python9.9/.security.json
            """
        ),
        captured.err,
    )


@dataclass
class endswith:
    """
    Assert that the str representation of the argument ends with the
    specfied suffix.
    """

    suffix: str

    def __eq__(self, actual):
        return str(actual).endswith(self.suffix)


def test_all_files(tmp_path, capsys):
    with mock_session(
        tmp_path / "artifacts",
        "9.9",
        "coverage-python9.9-fast/.coverage",
        "coverage-python9.9-slow/.coverage",
        "lint-python9.9/.lint.txt",
        "lint-python9.9/.lint.json",
        "security-python9.9/.security.json",
    ) as session:
        copy_artifacts(session)

    captured = capsys.readouterr()
    assert session.run.call_args == call(
        "coverage",
        "combine",
        "--keep",
        endswith("coverage-python9.9-fast/.coverage"),
        endswith("coverage-python9.9-slow/.coverage"),
    )
    assert re.match(
        cleandoc(
            f"""
            Copying file .*/lint-python9.9/.lint.txt
            Copying file .*/lint-python9.9/.lint.json
            Copying file .*/security-python9.9/.security.json
            """
        ),
        captured.err,
    )
    for f in [".lint.txt", ".lint.json", ".security.json"]:
        assert (tmp_path / f).exists()
