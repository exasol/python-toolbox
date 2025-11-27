import pytest
from pydantic_core._pydantic_core import ValidationError

from exasol.toolbox.config import (
    DEFAULT_EXCLUDED_PATHS,
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


def test_expansion_validation_fails_for_invalid_version():
    with pytest.raises(ValueError):
        BaseConfigExpansion(python_versions=("1.f.0",))


def test_minimum_python_version():
    conf = BaseConfig(python_versions=("5.5.5", "1.10", "9.9.9"))
    assert conf.minimum_python_version == "1.10"


@pytest.mark.parametrize("minimum_python_version", ["3.10", "3.10.5"])
def test_pyupgrade_argument(minimum_python_version):
    conf = BaseConfig(python_versions=("3.11", minimum_python_version, "3.12"))
    assert conf.pyupgrade_argument == ("--py310-plus",)


@pytest.mark.parametrize(
    "add_to_excluded_python_paths,expected",
    [
        pytest.param((), tuple(DEFAULT_EXCLUDED_PATHS), id="no_additions"),
        pytest.param(
            (next(iter(DEFAULT_EXCLUDED_PATHS)),),
            tuple(DEFAULT_EXCLUDED_PATHS),
            id="duplicate_addition",
        ),
        pytest.param(
            ("dummy",), tuple(DEFAULT_EXCLUDED_PATHS) + ("dummy",), id="add_a_new_entry"
        ),
    ],
)
def test_excluded_python_paths(add_to_excluded_python_paths, expected):
    conf = BaseConfig(add_to_excluded_python_paths=add_to_excluded_python_paths)
    assert sorted(conf.excluded_python_paths) == sorted(expected)
