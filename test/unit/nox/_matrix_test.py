from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from pydantic import computed_field

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._matrix import (
    _generate_matrix,
    generate_matrix,
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
