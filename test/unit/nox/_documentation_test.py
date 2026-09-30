import shutil
from unittest.mock import MagicMock, Mock, patch

import pytest
from nox.sessions import _SessionQuit

from exasol.toolbox.nox._documentation import (
    _build_docs,
    _build_multiversion_docs,
    _docs_list_links,
    _docs_links_check,
    build_docs,
    build_multiversion,
    clean_docs,
    docs_links_check,
    docs_list_links,
    open_docs,
)
from exasol.toolbox.nox._shared import DOCS_OUTPUT_DIR
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def index(config):
    index_rst = config.documentation_path / "index.rst"
    text = """
    .. _Test:

    Test
    ____test_docs_links

    .. toctree::
       :maxdepth: 1
       :hidden:

       dummy
   """
    index_rst.write_text(text)


@pytest.fixture
def config(test_project_config_factory):
    config = test_project_config_factory()

    # set up required file for Sphinx
    doc_path = config.documentation_path
    doc_path.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PROJECT_CONFIG.documentation_path / "conf.py", doc_path / "conf.py")

    return config


@pytest.fixture
def set_up_doc_with_link(config, index):
    dummy_rst = config.documentation_path / "dummy.rst"
    dummy_rst.write_text("https://examle.invalid\n:ref:`Test`")


class TestDocsListLinks:
    @pytest.mark.slow
    @staticmethod
    def test_works_as_expected(nox_session, config, set_up_doc_with_link, capsys):
        with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
            docs_list_links(nox_session)
        assert (
            capsys.readouterr().out
            == "filename: dummy.rst:1 -> uri: https://examle.invalid\n"
        )

    @staticmethod
    def test_raises_error_for_rcode_not_0(nox_session, config):
        with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
            with patch("exasol.toolbox.nox._documentation._docs_list_links") as mock:
                mock.return_value = (1, "dummy_text")

                with pytest.raises(_SessionQuit):
                    docs_list_links(nox_session)


def test_build_docs_runs_sphinx(nox_session, config):
    with patch("exasol.toolbox.nox._documentation._build_docs") as build:
        with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
            build_docs(nox_session)

    build.assert_called_once_with(nox_session, config)


def test_build_multiversion_docs_runs_sphinx(nox_session, config):
    with patch(
        "exasol.toolbox.nox._documentation._build_multiversion_docs"
    ) as build:
        with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
            build_multiversion(nox_session)

    build.assert_called_once_with(nox_session, config)


def test_build_docs_command(config):
    session = Mock()
    _build_docs(session, config)

    session.run.assert_called_once_with(
        "sphinx-build",
        "-W",
        "-b",
        "html",
        f"{config.documentation_path}",
        DOCS_OUTPUT_DIR,
    )


def test_build_multiversion_docs_commands(config):
    session = Mock()
    _build_multiversion_docs(session, config)

    assert session.run.call_count == 2
    session.run.assert_any_call(
        "sphinx-multiversion",
        f"{config.documentation_path}",
        DOCS_OUTPUT_DIR,
    )
    session.run.assert_any_call("touch", f"{DOCS_OUTPUT_DIR}/.nojekyll")


def test_open_docs_reports_missing_output(nox_session, config):
    with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
        with pytest.raises(_SessionQuit):
            open_docs(nox_session)


def test_open_docs_opens_index(nox_session, config):
    docs_folder = config.root_path / DOCS_OUTPUT_DIR
    docs_folder.mkdir()
    (docs_folder / "index.html").touch()
    with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
        with patch("exasol.toolbox.nox._documentation.webbrowser.open_new_tab") as open_tab:
            open_docs(nox_session)

    open_tab.assert_called_once_with((docs_folder / "index.html").as_uri())


def test_clean_docs_removes_output(nox_session, config):
    docs_folder = config.root_path / DOCS_OUTPUT_DIR
    docs_folder.mkdir()
    with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
        clean_docs(nox_session)

    assert not docs_folder.exists()


def test_docs_list_links_reports_sphinx_failure(tmp_path):
    with patch(
        "exasol.toolbox.nox._documentation.subprocess.run",
        return_value=MagicMock(returncode=2, stderr="sphinx failed"),
    ):
        result = _docs_list_links(tmp_path)

    assert result == (2, "sphinx failed")


@pytest.mark.slow
@pytest.mark.parametrize(
    "file_content, expected_code, expected_message",
    [
        ("https://github.com/exasol/python-toolbox", 0, ""),
        (
            "http://nox.thea.codes/en/stable/",
            0,
            "[redirected with Found] http://nox.thea.codes/en/stable/ to https://nox.thea.codes/en/stable/\n",
        ),
        (
            "https://github.com/exasol/python-toolbox/pull",
            0,
            "[redirected permanently] https://github.com/exasol/python-toolbox/pull to https://github.com/exasol/python-toolbox/pulls\n",
        ),
        (
            "https://github.com/exasol/python-toolbox/asdf",
            1,
            "[broken] https://github.com/exasol/python-toolbox/asdf: 404 Client Error: Not Found for url: https://github.com/exasol/python-toolbox/asdf\n",
        ),
    ],
)
def test_docs_links_check(config, index, file_content, expected_code, expected_message):
    dummy_rst = config.documentation_path / "dummy.rst"
    dummy_rst.write_text(file_content)

    args = MagicMock
    args.output = None

    code, message = _docs_links_check(config.documentation_path, args)

    assert code == expected_code
    assert expected_message in message


class TestDocsLinksCheck:
    @staticmethod
    def test_works_as_expected_for_good_link(nox_session, config):
        with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
            with patch("exasol.toolbox.nox._documentation._docs_links_check") as mock:
                mock.return_value = (0, "")
                docs_links_check(nox_session)

    @staticmethod
    def test_raises_exception_for_problem_returned(nox_session, config, capsys):
        with patch("exasol.toolbox.nox._documentation.PROJECT_CONFIG", new=config):
            with patch("exasol.toolbox.nox._documentation._docs_links_check") as mock:
                mock.return_value = (0, "[broken] ....")

                with pytest.raises(_SessionQuit):
                    docs_links_check(nox_session)

        assert capsys.readouterr().out == "\x1b[31merrors:\n[broken] ....\n"
