import pytest
import re
from inspect import cleandoc
from unittest.mock import Mock, patch
from exasol.toolbox.nox._artifacts import copy_artifacts



@pytest.fixture
def python_version():
    return "9.9"


@pytest.fixture
def project_config(python_version):
    with patch("exasol.toolbox.nox._artifacts.PROJECT_CONFIG") as config:
        config.python_versions = [python_version]
        yield config


def test_no_coverage(project_config, tmp_path, capsys):
    session = Mock(posargs=[str(tmp_path)])
    copy_artifacts(session)
    captured = capsys.readouterr()
    re.match(
        cleandoc(
            f"""
            Could not find any file .*/coverage-python9.9\\*/.coverage
            File not found .*/lint-python9.9/.lint.txt
            File not found .*/lint-python9.9/.lint.json
            File not found .*/security-python9.9/.security.json
            """
        ),
        captured.err,
    )
    with capsys.disabled():
        print(captured.err)
