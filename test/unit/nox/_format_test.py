from inspect import cleandoc
from unittest.mock import patch

import pytest
from nox.command import CommandFailed

from exasol.toolbox.nox._format import (
    _code_format,
    _pyupgrade,
    _ruff,
    fix,
    fmt_check,
)
from exasol.toolbox.nox._shared import Mode
from noxconfig import Config


@pytest.fixture
def file_with_unneeded_import(tmp_path):
    file_path = tmp_path / "dummy_file.py"
    file_path.write_text("import black")
    return file_path


@pytest.fixture
def file_with_not_ordered_import(tmp_path):
    file_path = tmp_path / "dummy_file.py"
    file_path.write_text("import isort\nimport black")
    return file_path


@pytest.fixture
def file_without_blank_line(tmp_path):
    file_path = tmp_path / "dummy_file.py"
    file_path.write_text("import black\nimport isort")
    return file_path


class TestCodeFormat:
    @staticmethod
    def test_isort_mode_fix(nox_session, file_with_not_ordered_import):
        _code_format(
            session=nox_session,
            mode=Mode.Fix,
            files=[str(file_with_not_ordered_import)],
        )
        assert (
            file_with_not_ordered_import.read_text() == "import black\nimport isort\n"
        )

    @staticmethod
    def test_isort_mode_check(nox_session, file_with_not_ordered_import, caplog):
        with pytest.raises(CommandFailed):
            _code_format(
                session=nox_session,
                mode=Mode.Check,
                files=[str(file_with_not_ordered_import)],
            )
        assert (
            caplog.messages[1]
            == f"Command isort --check {file_with_not_ordered_import} failed with exit code 1"
        )
        assert file_with_not_ordered_import.read_text() == "import isort\nimport black"

    @staticmethod
    def test_black_mode_fix(nox_session, file_without_blank_line):
        _code_format(
            session=nox_session,
            mode=Mode.Fix,
            files=[str(file_without_blank_line)],
        )
        assert file_without_blank_line.read_text() == "import black\nimport isort\n"

    @staticmethod
    def test_black_mode_check(nox_session, file_without_blank_line, caplog):
        with pytest.raises(CommandFailed):
            _code_format(
                session=nox_session,
                mode=Mode.Check,
                files=[str(file_without_blank_line)],
            )
        assert (
            caplog.messages[2]
            == f"Command black --check {file_without_blank_line} failed with exit code 1"
        )
        assert file_without_blank_line.read_text() == "import black\nimport isort"


def test_pyupgrade(nox_session, tmp_path):
    file_path = tmp_path / "dummy_file.py"
    file_path.write_text("from typing import Union\nx:Union[int, str]=2")
    _pyupgrade(session=nox_session, config=Config(), files=[str(file_path)])
    assert file_path.read_text() == "from typing import Union\nx:int | str=2"


class TestRuff:
    @staticmethod
    def test_mode_fix(nox_session, file_with_unneeded_import):
        _ruff(
            session=nox_session, mode=Mode.Fix, files=[str(file_with_unneeded_import)]
        )
        assert file_with_unneeded_import.read_text() == ""

    @staticmethod
    def test_mode_check(nox_session, file_with_unneeded_import, caplog):
        with pytest.raises(CommandFailed):
            _ruff(
                session=nox_session,
                mode=Mode.Check,
                files=[str(file_with_unneeded_import)],
            )
        assert (
            caplog.messages[1]
            == f"Command ruff check {file_with_unneeded_import} failed with exit code 1"
        )
        assert file_with_unneeded_import.read_text() == "import black"


@pytest.fixture
def file_with_multiple_problems(tmp_path):
    """
    In this file with multiple problems, it is expected that the nox session
    `format:fix` would alter the following:

    * x: Union[int, str]=2
       * This should be altered to `x: int | str = 2` via pyupgrade.
    * import isort
      * This should be removed via ruff as it is an unused import.
    * from typing import Union
       * This should be removed as pyupgrade has been executed and altered `x: Union[int, str]=2` to `x: int | str = 2`.
       * Thus, this is an unused import, which ruff will remove.
    * newlines and spaces added
       * black ensures that there is always:
           * a blank line between the imports and first executed line of code
           * a space around an equals sign, like ` = `.
           * a blank line at the end of a file
    """

    file_path = tmp_path / "dummy_file.py"
    text = """
    import numpy as np
    import isort # unused import
    from typing import Union
    x: Union[int, str]=2
    y: np.ndarray = np.array([1, 2, 3])
    """
    file_path.write_text(cleandoc(text))
    return file_path


def test_project_fix(nox_session, tmp_path, file_with_multiple_problems):
    with patch("exasol.toolbox.nox._format.PROJECT_CONFIG") as config:
        with patch("exasol.toolbox.nox._format._version") as version:
            config.root = tmp_path
            config.pyupgrade_argument = ("--py310-plus",)
            # Simulate version is up-to-date, as version check is out of the scope of the test case
            version.return_value = True
            fix(nox_session)

    assert (
        file_with_multiple_problems.read_text()
        == cleandoc(
            """
            import numpy as np

            x: int | str = 2
            y: np.ndarray = np.array([1, 2, 3])
        """
        )
        + "\n"
    )


def test_project_format(
    nox_session, tmp_path, file_with_multiple_problems, caplog, capsys
):
    expected_text = file_with_multiple_problems.read_text()

    with patch("exasol.toolbox.nox._format.PROJECT_CONFIG") as config:
        config.root = tmp_path
        with pytest.raises(CommandFailed):
            fmt_check(nox_session)

    # The failed message should always relate to the checking function called first.
    assert (
        caplog.messages[1]
        == f"Command ruff check {file_with_multiple_problems} failed with exit code 1"
    )
    # The file should not be changed.
    assert file_with_multiple_problems.read_text() == expected_text
