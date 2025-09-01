from toolbox.nox._lint import dist_check


class TestDistributionCheck:
    @staticmethod
    def test_works_as_expected(nox_session, capsys):
        dist_check(nox_session)
