import shutil
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest
from nox.sessions import _SessionQuit

from exasol.toolbox.nox._documentation import (
    _docs_links_check,
    docs_list_links,
)
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

       file
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
