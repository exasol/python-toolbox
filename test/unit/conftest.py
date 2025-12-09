import pytest

from exasol.toolbox.config import BaseConfig


@pytest.fixture
def test_project_config_factory(tmp_path):
    def _test_project_config(**kwargs) -> BaseConfig:
        defaults = {
            "root_path": tmp_path,
            "project_name": "test",
        }
        config = {**defaults, **kwargs}
        return BaseConfig(**config)

    return _test_project_config
