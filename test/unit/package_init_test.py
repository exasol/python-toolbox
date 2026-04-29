import exasol.toolbox
from exasol.toolbox.util.version import Version


def test_package_version_is_set():
    assert isinstance(exasol.toolbox.__version__, str)
    assert Version.from_string(exasol.toolbox.__version__)
