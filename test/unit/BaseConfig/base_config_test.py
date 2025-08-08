import pydantic
import pytest

from exasol.toolbox.BaseConfig import (
    BaseConfig,
    str_like_version_validation,
)


@pytest.mark.parametrize(
    "versions", (["$.2.3"], ["1.f.1"], ["1.1.1", "1.2.3", "2.3.4", "2.3.7", "1.1.1.1"])
)
def test_str_like_version_validation(versions):
    with pytest.raises(ValueError):
        str_like_version_validation(versions)


def test_default():
    config = BaseConfig()
    str_like_version_validation(config.python_versions)
    str_like_version_validation(config.exasol_versions)


def test_new_value():
    conf = BaseConfig(python_versions=["1.21.1", "1.1.1"])
    assert conf.python_versions == ["1.21.1", "1.1.1"]


class BaseConfigExpansion(BaseConfig):
    expansion1: str = "test1"


def test_expansion_validation():
    with pytest.raises(ValueError):
        _ = BaseConfigExpansion(python_versions=["1.1.1", "1.1.F"])


def test_min_max_py():
    conf = BaseConfig(python_versions=["1.1.1", "5.5.5", "9.9.9"])
    assert conf.min_py_version == "1.1.1" and conf.max_py_version == "9.9.9"
