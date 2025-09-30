import shutil
from pathlib import Path
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest
from nox.command import CommandFailed

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._package import (
    PROJECT_CONFIG,
    package_check,
)


class TestDistributionCheck:
    @staticmethod
    def test_works_as_expected(nox_session):
        package_check(nox_session)

    @staticmethod
    def test_raises_non_zero_exist_with_readme_error(nox_session, tmp_path):
        # TODOs
        # 1. copy package files to a temp directory
        # 2. mock/alter the path for the function you need to use for testing
        # 3. modify rst file to have a broken link like is in this commit:
        #     - `Python <https://www.python.org/`__ >= 3.9
        package = Path(tmp_path)
        package_readme = package / "README.rst"
        shutil.copytree(PROJECT_CONFIG.root / "exasol", package / "exasol")
        shutil.copyfile(PROJECT_CONFIG.root / "README.rst", package_readme)
        shutil.copytree(PROJECT_CONFIG.root / "doc/changes", package / "doc/changes")
        shutil.copyfile(PROJECT_CONFIG.root / "LICENSE", package / "LICENSE")
        shutil.copyfile(
            PROJECT_CONFIG.root / "pyproject.toml", package / "pyproject.toml"
        )
        old = "- `Python <https://www.python.org/>`__ >= 3.9"
        error = "- `Python <https://www.python.org/>`__ >= 3.9"
        readme = package_readme.read_text().splitlines()
        error_readme = [error if old in line else line for line in readme]
        package_readme.write_text("/n".join(error_readme))
        config = BaseConfig()
        mock = MagicMock(spec=BaseConfig, wraps=config)
        mock.root = package
        with pytest.raises(CommandFailed) as e:
            with patch("exasol.toolbox.nox._package.PROJECT_CONFIG", mock):
                print(PROJECT_CONFIG.root)
                package_check(nox_session)
        # verify broken with non-zero exit status
        assert str(e.value) == "Returned code 1"
