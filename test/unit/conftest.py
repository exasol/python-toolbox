from pathlib import Path

import pytest
from toolbox.config import BaseConfig


@pytest.fixture
def test_project_config():
    return BaseConfig(root_path=Path("."), project_name="test")
