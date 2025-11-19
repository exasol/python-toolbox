import pytest
from nox.command import CommandFailed
from toolbox.nox._format import _ruff

from exasol.toolbox.nox._shared import Mode


@pytest.fixture
def file_with_unneeded_import(tmp_path):
    file_path = tmp_path / "dummy_file.py"
    file_path.write_text("import black")
    return file_path


class TestRuff:
    @staticmethod
    def test_mode_fix(nox_session, file_with_unneeded_import):
        _ruff(
            session=nox_session, mode=Mode.Fix, files=[str(file_with_unneeded_import)]
        )
        assert file_with_unneeded_import.read_text() == ""

    @staticmethod
    def test_mode_check(nox_session, file_with_unneeded_import):
        with pytest.raises(CommandFailed):
            _ruff(
                session=nox_session,
                mode=Mode.Check,
                files=[str(file_with_unneeded_import)],
            )
        assert file_with_unneeded_import.read_text() == "import black"
