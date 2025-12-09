import shutil
from pathlib import Path
from unittest.mock import (
    patch,
)

import pytest
from nox.command import CommandFailed

from exasol.toolbox.nox._package import (
    PROJECT_CONFIG,
    package_check,
)


class TestDistributionCheck:
    @staticmethod
    def test_works_as_expected(nox_session):
        package_check(nox_session)

    @staticmethod
    def test_raises_non_zero_exist_with_readme_error(
        nox_session, test_project_config_factory, tmp_path
    ):
        package = Path(tmp_path)
        package_readme = package / "README.rst"

        # copy over `packages` and `include` from `pyproject.toml` to for `poetry build`
        shutil.copytree(PROJECT_CONFIG.root_path / "exasol", package / "exasol")
        shutil.copyfile(PROJECT_CONFIG.root_path / "README.rst", package_readme)
        shutil.copytree(
            PROJECT_CONFIG.root_path / "doc/changes", package / "doc/changes"
        )
        shutil.copyfile(PROJECT_CONFIG.root_path / "LICENSE", package / "LICENSE")
        shutil.copyfile(
            PROJECT_CONFIG.root_path / "pyproject.toml", package / "pyproject.toml"
        )

        # create an error in readme.rst
        not_closed_link_error = "- `Python <https://www.python.org/`__ >= 3.9"
        package_readme.open(mode="a").write(not_closed_link_error)

        # use of the folder with errors in the nox -s package:check function
        with pytest.raises(CommandFailed) as e:
            with patch(
                "exasol.toolbox.nox._package.PROJECT_CONFIG",
                new=test_project_config_factory(),
            ):
                package_check(nox_session)
        # verify broken with non-zero exit status
        assert str(e.value) == "Returned code 1"
