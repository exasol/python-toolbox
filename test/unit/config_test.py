import pytest
from pydantic_core._pydantic_core import ValidationError

from exasol.toolbox.config import (
    BaseConfig,
    valid_version_string,
)


class TestBaseConfig:
    @staticmethod
    def test_works_as_defined():
        BaseConfig()

    @staticmethod
    @pytest.mark.parametrize(
        "wrong_input,expected_message",
        [
            pytest.param(
                {"python_versions": ["1.2.3.1"]},
                "Version has an invalid format",
                id="python_versions",
            ),
            pytest.param(
                {"exasol_versions": ["1.2.3.1"]},
                "Version has an invalid format",
                id="exasol_versions",
            ),
        ],
    )
    def test_raises_exception_when_incorrect_modification(
        wrong_input: dict, expected_message: str
    ):
        with pytest.raises(ValidationError, match=expected_message):
            BaseConfig(**wrong_input)


class TestValidVersionString:
    @staticmethod
    def test_work_as_expected():
        version_string = "1.2.3"
        result = valid_version_string(version_string=version_string)
        assert result == version_string

    @staticmethod
    def test_raises_exception_when_not_valid():
        with pytest.raises(ValueError):
            valid_version_string("$.2.3")


class BaseConfigExpansion(BaseConfig):
    expansion1: str = "test1"


def test_expansion_validation():
    with pytest.raises(ValueError):
        _ = BaseConfigExpansion(python_versions=("1.f.0",))

def test_min_py_version():
    conf = BaseConfig(python_versions=("5.5.5", "1.1.1", "9.9.9"))
    assert conf.min_py_version == "1.1.1"
