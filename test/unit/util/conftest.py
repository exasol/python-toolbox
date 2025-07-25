from collections import OrderedDict

import pytest

from exasol.toolbox.util.dependencies.poetry_dependencies import PoetryGroup
from exasol.toolbox.util.dependencies.shared_models import Package


@pytest.fixture(scope="module")
def main_group():
    return PoetryGroup(name="main", toml_section="project.dependencies")


@pytest.fixture(scope="module")
def dev_group():
    return PoetryGroup(name="dev", toml_section="tool.poetry.group.dev.dependencies")


@pytest.fixture(scope="module")
def previous_dependencies(main_group, dev_group):
    deps = OrderedDict()
    deps[main_group.name] = {"package1": Package(name="package1", version="0.0.1")}
    return deps


@pytest.fixture(scope="module")
def dependencies(main_group, dev_group):
    deps = OrderedDict()
    deps[main_group.name] = {"package1": Package(name="package1", version="0.1.0")}
    deps[dev_group.name] = {"package2": Package(name="package2", version="0.2.0")}
    return deps
