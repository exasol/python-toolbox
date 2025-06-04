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

from exasol.toolbox.nox._artifacts import (
    ALL_FILES,
    COVERAGE_FILE,
    LINT_JSON,
    _missing_files,
    copy_artifacts,
)


@contextlib.contextmanager
def mock_session(path: Path, python_version: str, *files: str):
    with patch("exasol.toolbox.nox._artifacts.PROJECT_CONFIG") as config:
        config.python_versions = [python_version]
        for rel in files:
            file = path / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(rel)
        yield Mock(posargs=[str(path)])


@dataclass
class EndsWith:
    """
    Assert that the str representation of the argument ends with the
    specified suffix.
    """

    suffix: str

    def __eq__(self, actual):
        return str(actual).endswith(self.suffix)


@pytest.mark.parametrize(
    "missing_files",
    [
        (pytest.param(set(), id="all_files_present")),
        (pytest.param({LINT_JSON}, id="lint_json_missing")),
        (pytest.param({LINT_JSON, COVERAGE_FILE}, id="coverage_and_lint_json_missing")),
        (pytest.param(ALL_FILES, id="all_files_missing")),
    ],
)
def test_missing_files(missing_files, tmp_path):
    existing_files = ALL_FILES - missing_files
    path = Path(tmp_path)
    for file in existing_files:
        Path(path, file).touch()

    actual = _missing_files(ALL_FILES, path)
    assert actual == missing_files


class TestCopyArtifacts:
    @staticmethod
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

    @staticmethod
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
            EndsWith("coverage-python9.9-fast/.coverage"),
            EndsWith("coverage-python9.9-slow/.coverage"),
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
