import os.path
import posixpath
from unittest.mock import Mock

import pytest

from exasol.toolbox.sphinx.multiversion.sphinx import VersionInfo


@pytest.fixture
def version_info(tmp_path):
    root = tmp_path

    mock = Mock()
    myapp = mock.config
    myapp.config.project = "example"

    return VersionInfo(
        app=myapp,
        context={"pagename": "testpage"},
        metadata={
            "master": {
                "name": "master",
                "version": "",
                "release": "0.2",
                "is_released": False,
                "source": "heads",
                "creatordate": "2020-08-07 07:45:20 -0700",
                "basedir": os.path.join(root, "master"),
                "sourcedir": os.path.join(root, "master", "docs"),
                "outputdir": os.path.join(root, "build", "html", "master"),
                "confdir": os.path.join(root, "master", "docs"),
                "docnames": ["testpage", "appendix/faq"],
                "build_targets": {
                    "HTML": {
                        "builder": "html",
                        "downloadable": True,
                        "download_format": "zip",
                    },
                },
            },
            "v0.1.0": {
                "name": "v0.1.0",
                "version": "",
                "release": "0.1.0",
                "is_released": True,
                "source": "tags",
                "creatordate": "2020-07-16 08:45:20 -0100",
                "basedir": os.path.join(root, "v0.1.0"),
                "sourcedir": os.path.join(root, "v0.1.0", "docs"),
                "outputdir": os.path.join(root, "build", "html", "v0.1.0"),
                "confdir": os.path.join(root, "v0.1.0", "docs"),
                "docnames": ["old_testpage", "appendix/faq"],
                "build_targets": {
                    "HTML": {
                        "builder": "html",
                        "downloadable": True,
                        "download_format": "zip",
                    },
                },
            },
            "branch-with/slash": {
                "name": "branch-with/slash",
                "version": "",
                "release": "0.1.1",
                "is_released": False,
                "source": "heads",
                "creatordate": "2020-08-06 11:53:06 -0400",
                "basedir": os.path.join(root, "branch-with/slash"),
                "sourcedir": os.path.join(root, "branch-with/slash", "docs"),
                "outputdir": os.path.join(root, "build", "html", "branch-with/slash"),
                "confdir": os.path.join(root, "branch-with/slash", "docs"),
                "docnames": ["testpage"],
                "build_targets": {
                    "HTML": {
                        "builder": "html",
                        "downloadable": True,
                        "download_format": "zip",
                    },
                },
            },
        },
        current_version_name="master",
    )


def test_tags_property(version_info):
    versions = version_info.tags
    assert {version.name for version in versions} == {"v0.1.0"}


def test_branches_property(version_info):
    versions = version_info.branches
    assert {version.name for version in versions} == {"master", "branch-with/slash"}


def test_releases_property(version_info):
    versions = version_info.releases
    assert {version.name for version in versions} == {"v0.1.0"}


def test_in_development_property(version_info):
    versions = version_info.in_development
    assert {version.name for version in versions} == {"master", "branch-with/slash"}


def test_vhasdoc(version_info):
    assert version_info.vhasdoc("master")
    assert not version_info.vhasdoc("v0.1.0")
    assert version_info.vhasdoc("branch-with/slash")

    version_info.context["pagename"] = "appendix/faq"

    assert version_info.vhasdoc("master")
    assert version_info.vhasdoc("v0.1.0")
    assert not version_info.vhasdoc("branch-with/slash")


def test_vpathto(version_info):
    assert version_info.vpathto("master") == "testpage.html"
    assert version_info.vpathto("v0.1.0") == posixpath.join(
        "..", "v0.1.0", "index.html"
    )
    assert version_info.vpathto("branch-with/slash") == posixpath.join(
        "..", "branch-with/slash", "testpage.html"
    )

    version_info.context["pagename"] = "appendix/faq"

    assert version_info.vpathto("master") == "faq.html"
    assert version_info.vpathto("v0.1.0") == posixpath.join(
        "..", "..", "v0.1.0", "appendix", "faq.html"
    )
    assert version_info.vpathto("branch-with/slash") == posixpath.join(
        "..", "..", "branch-with/slash", "index.html"
    )


def test_apathto(version_info):
    build_targets = {
        "HTML": {
            "builder": "html",
            "downloadable": True,
            "download_format": "zip",
        },
        "PDF": {
            "builder": "latexpdf",
            "downloadable": True,
            "download_format": "pdf",
        },
    }
    assert version_info.apathto("HTML", build_targets["HTML"]) == posixpath.join(
        "artefacts", "example_docs-master-HTML.zip"
    )
    assert version_info.apathto("PDF", build_targets["PDF"]) == posixpath.join(
        "artefacts", "example_docs-master.pdf"
    )

    version_info.context["pagename"] = "appendix/faq"
    assert version_info.apathto("PDF", build_targets["PDF"]) == posixpath.join(
        "..", "artefacts", "example_docs-master.pdf"
    )

    version_info.context["pagename"] = "testpage"
    version_info.current_version_name = "branch-with/slash"

    assert version_info.apathto("PDF", build_targets["PDF"]) == posixpath.join(
        "artefacts", "example_docs-branch-with-slash.pdf"
    )
    assert version_info.apathto("HTML", build_targets["HTML"]) == posixpath.join(
        "artefacts", "example_docs-branch-with-slash-HTML.zip"
    )

    version_info.app.config.project = "Project Name with Spaces and VaRiAbLe case"
    version_info.current_version_name = "master"
    assert version_info.apathto("HTML", build_targets["HTML"]) == posixpath.join(
        "artefacts",
        "ProjectNamewithSpacesandVaRiAbLecase_docs-master-HTML.zip",
    )
    assert version_info.apathto("PDF", build_targets["PDF"]) == posixpath.join(
        "artefacts",
        "ProjectNamewithSpacesandVaRiAbLecase_docs-master.pdf",
    )
