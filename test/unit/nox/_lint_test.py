import pytest
from nox.command import CommandFailed
from toolbox.nox._lint import dist_check


class TestDistributionCheck:
    @staticmethod
    def test_works_as_expected(nox_session):
        dist_check(nox_session)

    @staticmethod
    def test_raises_non_zero_exist_with_readme_error(nox_session):
        # TODOs
        # 1. copy package files to a temp directory
        # 2. mock/alter the path for the function you need to use for testing
        # 3. modify rst file to have a broken link like is in this commit:
        #     - `Python <https://www.python.org/`__ >= 3.9

        with pytest.raises(CommandFailed) as e:
            dist_check(nox_session)
        # verify broken with non-zero exit status
        assert str(e.value) == "Returned code 1"
