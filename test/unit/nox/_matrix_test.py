from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from pydantic import computed_field

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._matrix import (
    exasol_matrix,
    full_matrix,
    generate_matrix,
    _generate_matrix,
    python_matrix,
)


@pytest.fixture
def nox_session_runner_posargs(request) -> list[str]:
    return list(getattr(request, "param", []))


@pytest.fixture
def config(tmp_path) -> BaseConfig:
    class Config(BaseConfig):
        extra_matrix_value: str = "extra"

        @computed_field  # type: ignore[misc]
        @property
        def computed_matrix_value(self) -> str:
            return f"{self.project_name}-computed"

    return Config(root_path=tmp_path, project_name="toolbox")


class TestGenerateMatrix:
    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        [["computed_matrix_value", "extra_matrix_value"]],
        indirect=True,
    )
    def test_uses_requested_field_names(
        nox_session,
        config,
        capsys,
        nox_session_runner_posargs,
    ):
        with patch("exasol.toolbox.nox._matrix.PROJECT_CONFIG", new=config):
            generate_matrix(nox_session)

        assert json.loads(capsys.readouterr().out) == {
            "computed_matrix_value": ["toolbox-computed"],
            "extra_matrix_value": ["extra"],
        }

    @staticmethod
    @pytest.mark.parametrize(
        "nox_session_runner_posargs",
        [["missing_value"]],
        indirect=True,
    )
    def test_rejects_unknown_field(
        nox_session,
        config,
        capsys,
        nox_session_runner_posargs,
    ):
        with patch("exasol.toolbox.nox._matrix.PROJECT_CONFIG", new=config):
            with pytest.raises(SystemExit):
                generate_matrix(nox_session)

        assert "invalid choice: 'missing_value'" in capsys.readouterr().err


class TestGenerateMatrixHelper:
    @staticmethod
    @pytest.mark.parametrize(
        ("requested_keys", "expected"),
        [
            (
                ("computed_matrix_value",),
                {"computed_matrix_value": ["toolbox-computed"]},
            ),
            (
                ("computed_matrix_value", "extra_matrix_value"),
                {
                    "computed_matrix_value": ["toolbox-computed"],
                    "extra_matrix_value": ["extra"],
                },
            ),
        ],
    )
    def test_returns_requested_keys(config, requested_keys, expected):
        assert _generate_matrix(config, requested_keys) == expected

    @staticmethod
    def test_rejects_unknown_key(config):
        with pytest.raises(KeyError, match="missing_matrix_value"):
            _generate_matrix(config, ("missing_matrix_value",))


class TestDeprecatedMatrixSessions:
    @staticmethod
    def test_exasol_session_still_emits_field_names(
        nox_session, config, caplog, capsys
    ):
        with patch("exasol.toolbox.nox._matrix.PROJECT_CONFIG", new=config):
            exasol_matrix(nox_session)

        captured = capsys.readouterr()
        assert json.loads(captured.out) == {
            "exasol-version": ["7.1.30", "8.29.13", "2025.1.8"]
        }
        assert len(caplog.messages) == 1

    @staticmethod
    def test_python_session_still_emits_field_names(
        nox_session, config, caplog, capsys
    ):
        with patch("exasol.toolbox.nox._matrix.PROJECT_CONFIG", new=config):
            python_matrix(nox_session)

        captured = capsys.readouterr()
        assert json.loads(captured.out) == {
            "python-version": ["3.10", "3.11", "3.12", "3.13", "3.14"]
        }
        assert len(caplog.messages) == 1

    @staticmethod
    def test_full_session_still_emits_field_names(nox_session, config, caplog, capsys):
        with patch("exasol.toolbox.nox._matrix.PROJECT_CONFIG", new=config):
            full_matrix(nox_session)

        captured = capsys.readouterr()
        assert json.loads(captured.out) == {
            "python-version": ["3.10", "3.11", "3.12", "3.13", "3.14"],
            "exasol-version": ["7.1.30", "8.29.13", "2025.1.8"],
        }
        assert len(caplog.messages) == 1
