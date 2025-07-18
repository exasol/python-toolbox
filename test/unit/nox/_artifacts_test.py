import contextlib
import json
import re
import sqlite3
from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path
from typing import Any
from unittest import mock
from unittest.mock import (
    Mock,
    call,
    patch,
)

import pytest
from nox import (
    Session,
    _options,
    manifest,
    virtualenv,
)
from nox.sessions import (
    SessionRunner,
    _SessionQuit,
)

from exasol.toolbox.nox import _artifacts
from exasol.toolbox.nox._artifacts import (
    ALL_LINT_FILES,
    COVERAGE_DB,
    COVERAGE_TABLES,
    COVERAGE_XML,
    LINT_JSON,
    LINT_JSON_ATTRIBUTES,
    LINT_TXT,
    SECURITY_JSON,
    SECURITY_JSON_ATTRIBUTES,
    _is_valid_coverage,
    _is_valid_lint_json,
    _is_valid_lint_txt,
    _is_valid_security_json,
    _prepare_coverage_xml,
    check_artifacts,
    copy_artifacts,
)


@contextlib.contextmanager
def mock_check_artifacts_session(
    path: Path,
):
    with patch("exasol.toolbox.nox._artifacts.PROJECT_CONFIG") as config:
        config.root = path
        yield Mock()


@contextlib.contextmanager
def mock_session(path: Path, python_version: str, *files: str):
    with patch("exasol.toolbox.nox._artifacts.PROJECT_CONFIG") as config:
        config.python_versions = [python_version]
        for rel in files:
            file = path / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(rel)
        yield Mock(posargs=[str(path)])


def _create_coverage_file(path: Path, tables: set) -> None:
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (test INTEGER)")


@dataclass
class EndsWith:
    """
    Assert that the str representation of the argument ends with the
    specified suffix.
    """

    suffix: str

    def __eq__(self, actual):
        return str(actual).endswith(self.suffix)


class TestCheckArtifacts:
    @staticmethod
    def _create_artifact_files(path: Path, existing_files: set):
        for file in existing_files:
            Path(path, file).touch()

    @mock.patch("exasol.toolbox.nox._artifacts._is_valid_lint_txt", return_value=True)
    @mock.patch("exasol.toolbox.nox._artifacts._is_valid_lint_json", return_value=True)
    @mock.patch(
        "exasol.toolbox.nox._artifacts._is_valid_security_json", return_value=True
    )
    @mock.patch("exasol.toolbox.nox._artifacts._is_valid_coverage", return_value=True)
    def test_passes_when_as_expected(
        self, mock_coverage, mock_security, mock_lint_json, mock_lint_txt, tmp_path
    ):
        self._create_artifact_files(tmp_path, ALL_LINT_FILES)
        with mock_check_artifacts_session(tmp_path) as session:
            check_artifacts(session)

    @pytest.mark.parametrize(
        "missing_files",
        [
            (pytest.param({LINT_JSON}, id="lint_json_missing")),
            (pytest.param(ALL_LINT_FILES, id="all_files_missing")),
        ],
    )
    def test_fails_when_file_missing(self, tmp_path, missing_files, capsys):
        existing_files = ALL_LINT_FILES - missing_files
        self._create_artifact_files(tmp_path, existing_files)

        with mock_check_artifacts_session(tmp_path) as session:
            with pytest.raises(SystemExit):
                check_artifacts(session)
        assert f"files not available: {missing_files}" in capsys.readouterr().err

    def test_fails_when_check_fails(self, tmp_path, capsys):
        self._create_artifact_files(tmp_path, ALL_LINT_FILES)
        with mock_check_artifacts_session(tmp_path) as session:
            with pytest.raises(SystemExit):
                check_artifacts(session)
        assert "error in [" in capsys.readouterr().err


class TestIsValidLintTxt:
    @staticmethod
    def _create_json_txt(path: Path, text: str) -> None:
        path.touch()
        path.write_text(text)

    def test_passes_when_as_expected(self, tmp_path):
        path = Path(tmp_path, LINT_TXT)
        text = "Your code has been rated at 7.85/10 (previous run: 7.83/10, +0.02"
        self._create_json_txt(path, text)

        assert _is_valid_lint_txt(path)

    def test_fails_when_rating_not_found(self, tmp_path, capsys):
        path = Path(tmp_path, LINT_TXT)
        text = "dummy_text"
        self._create_json_txt(path, text)

        result = _is_valid_lint_txt(path)

        assert not result
        assert "Could not find a rating" in capsys.readouterr().err


class TestIsValidLintJson:
    @staticmethod
    def _create_expected_json_file(path: Path, attributes: set) -> None:
        path.touch()
        attributes_dict = {attribute: None for attribute in attributes}
        with path.open("w") as file:
            json.dump([attributes_dict], file)

    def test_passes_when_as_expected(self, tmp_path):
        path = Path(tmp_path, LINT_JSON)
        self._create_expected_json_file(path, attributes=LINT_JSON_ATTRIBUTES)

        result = _is_valid_lint_json(path)
        assert result

    @staticmethod
    def test_is_not_a_json(tmp_path, capsys):
        path = Path(tmp_path, LINT_JSON)
        path.touch()
        path.write_text("dummy")

        result = _is_valid_lint_json(path)

        assert not result
        assert "Invalid json file" in capsys.readouterr().err

    @pytest.mark.parametrize(
        "missing_attributes", [pytest.param({"message-id"}, id="missing_message-id")]
    )
    def test_missing_attributes(self, tmp_path, capsys, missing_attributes):
        attributes = LINT_JSON_ATTRIBUTES - missing_attributes
        path = Path(tmp_path, LINT_JSON)
        self._create_expected_json_file(path, attributes=attributes)

        result = _is_valid_lint_json(path)

        assert not result
        assert (
            f"missing the following attributes {missing_attributes}"
            in capsys.readouterr().err
        )


class TestIsValidSecurityJson:
    @staticmethod
    def _create_expected_json_file(path: Path, attributes: set) -> None:
        path.touch()
        attributes_dict = {attribute: None for attribute in attributes}
        with path.open("w") as file:
            json.dump(attributes_dict, file)

    def test_passes_when_as_expected(self, tmp_path):
        path = Path(tmp_path, SECURITY_JSON)
        self._create_expected_json_file(path, attributes=SECURITY_JSON_ATTRIBUTES)

        assert _is_valid_security_json(path)

    @staticmethod
    def test_is_not_a_json(tmp_path, capsys):
        path = Path(tmp_path, LINT_JSON)
        path.touch()
        path.write_text("dummy")

        result = _is_valid_security_json(path)

        assert not result
        assert "Invalid json file" in capsys.readouterr().err

    @pytest.mark.parametrize(
        "missing_attributes", [pytest.param({"errors"}, id="missing_errors")]
    )
    def test_missing_attributes(self, tmp_path, capsys, missing_attributes):
        attributes = SECURITY_JSON_ATTRIBUTES - missing_attributes
        path = Path(tmp_path, LINT_JSON)
        self._create_expected_json_file(path, attributes=attributes)

        result = _is_valid_security_json(path)

        assert not result
        assert (
            f"missing the following attributes {missing_attributes}"
            in capsys.readouterr().err
        )


class TestIsValidCoverage:
    def test_passes_when_as_expected(self, tmp_path):
        path = Path(tmp_path, COVERAGE_DB)
        _create_coverage_file(path, COVERAGE_TABLES)

        result = _is_valid_coverage(path)

        assert result

    @pytest.mark.parametrize(
        "missing_table",
        [
            pytest.param({"coverage_schema"}, id="missing_coverage_schema"),
        ],
    )
    def test_database_missing_tables(self, tmp_path, capsys, missing_table):
        tables = COVERAGE_TABLES - missing_table
        path = Path(tmp_path, COVERAGE_DB)
        _create_coverage_file(path, tables)

        result = _is_valid_coverage(path)

        assert not result
        assert (
            f"missing the following tables {missing_table}" in capsys.readouterr().err
        )


class TestCopyArtifacts:
    @staticmethod
    def test_missing_files(tmp_path, capsys):
        with mock_session(tmp_path, "9.9") as session:
            copy_artifacts(session)
        captured = capsys.readouterr()
        assert re.match(
            cleandoc(
                """
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
                """
                Copying file .*/lint-python9.9/.lint.txt
                Copying file .*/lint-python9.9/.lint.json
                Copying file .*/security-python9.9/.security.json
                """
            ),
            captured.err,
        )
        for f in [".lint.txt", ".lint.json", ".security.json"]:
            assert (tmp_path / f).exists()


class FakeEnv(mock.MagicMock):
    # Extracted from nox testing
    _get_env = virtualenv.VirtualEnv._get_env


def make_fake_env(venv_backend: str = "venv", **kwargs: Any) -> FakeEnv:
    # Extracted from nox testing
    return FakeEnv(
        spec=virtualenv.VirtualEnv,
        env={},
        venv_backend=venv_backend,
        **kwargs,
    )


@pytest.fixture
def nox_session(tmp_path):
    # Extracted from nox testing
    session_runner = SessionRunner(
        name="test",
        signatures=["test"],
        func=mock.Mock(spec=["python"], python="3.10"),
        global_config=_options.options.namespace(
            posargs=[],
            error_on_external_run=False,
            install_only=False,
            invoked_from=tmp_path,
        ),
        manifest=mock.create_autospec(manifest.Manifest),
    )
    session_runner.venv = make_fake_env(bin_paths=["/no/bin/for/you"])
    session = Session(session_runner)
    yield session


class TestPrepareCoverageXml:
    @staticmethod
    def test_no_coverage_file_silently_passes(monkeypatch, tmp_path, nox_session):
        coverage_xml = tmp_path / COVERAGE_XML
        coverage_db = tmp_path / COVERAGE_DB
        monkeypatch.setattr(_artifacts, "COVERAGE_XML", coverage_xml)

        _prepare_coverage_xml(nox_session, tmp_path, cwd=tmp_path)

        assert not Path(coverage_db).exists()
        assert not Path(coverage_xml).exists()

    @staticmethod
    def test_that_bad_coverage_file_still_raises_error(
        monkeypatch, tmp_path, nox_session
    ):
        coverage_xml = tmp_path / COVERAGE_XML
        coverage_db = tmp_path / COVERAGE_DB
        monkeypatch.setattr(_artifacts, "COVERAGE_XML", coverage_xml)
        _create_coverage_file(coverage_db, COVERAGE_TABLES)

        with pytest.raises(
            _SessionQuit, match="doesn't seem to be a coverage data file"
        ):
            _prepare_coverage_xml(nox_session, tmp_path, cwd=tmp_path)

        assert coverage_db.exists()
        assert not coverage_xml.exists()
