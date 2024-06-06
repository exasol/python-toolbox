import os

import pytest


@pytest.fixture
def temporary_directory(tmp_path):
    old = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old)
