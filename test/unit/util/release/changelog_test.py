from datetime import datetime
from inspect import cleandoc
from unittest.mock import Mock

import pytest

import exasol.toolbox.util.release.changelog as impl
from exasol.toolbox.util.dependencies.shared_models import LatestTagNotFoundError
from exasol.toolbox.util.release.changelog import (
    UNRELEASED_INITIAL_CONTENT,
    Changelogs,
)
from exasol.toolbox.util.version import Version


class SampleContent:
    changelog = "\n" + cleandoc("""
        Summary of changes.

        ## Added
        * Added Awesome feature

        ## Changed
        * Some behaviour

        ## Fixed
        * Fixed nasty bug
        """)
    changes = cleandoc("""
        # Changelog

        * [unreleased](unreleased.md)
        * [0.1.0](changes_0.1.0.md)

        ```{toctree}
        ---
        hidden:
        ---
        unreleased
        changes_0.1.0
        ```
        """)
    altered_changes = cleandoc("""
        # Changelog

        * [unreleased](unreleased.md)
        * [1.0.0](changes_1.0.0.md)
        * [0.1.0](changes_0.1.0.md)

        ```{toctree}
        ---
        hidden:
        ---
        unreleased
        changes_1.0.0
        changes_0.1.0
        ```
        """)


def expected_changes_file_content(with_dependencies: bool = False):
    header = cleandoc(f"""
        # 1.0.0 - {datetime.today().strftime('%Y-%m-%d')}

        ## Summary

        Summary of changes.

        ## Added
        * Added Awesome feature

        ## Changed
        * Some behaviour

        ## Fixed
        * Fixed nasty bug
        """)
    dependencies = cleandoc(f"""
        ## Dependency Updates

        ### `main`

        * Updated dependency `package1:0.0.1` to `0.1.0`

        ### `dev`

        * Added dependency `package2:0.2.0`
        """)
    return f"{header}\n\n{dependencies}\n" if with_dependencies else f"{header}\n"


@pytest.fixture(scope="function")
def changes_md(changelogs):
    changelogs.changelog_md.write_text(SampleContent.changes)


@pytest.fixture(scope="function")
def unreleased_md(changelogs):
    changelogs.unreleased_md.write_text(
        UNRELEASED_INITIAL_CONTENT + SampleContent.changelog
    )


def mock_changelog(monkeypatch, old_dependencies, new_dependencies):
    for func, value in (
        ("get_dependencies_from_latest_tag", old_dependencies),
        ("get_dependencies", new_dependencies),
    ):
        mock = value if isinstance(value, Mock) else Mock(return_value=value)
        monkeypatch.setattr(impl, func, mock)


@pytest.fixture(scope="function")
def mock_dependencies(monkeypatch, previous_dependencies, dependencies):
    mock_changelog(monkeypatch, previous_dependencies, dependencies)


@pytest.fixture(scope="function")
def mock_new_dependencies(monkeypatch, dependencies):
    mock_changelog(monkeypatch, Mock(side_effect=LatestTagNotFoundError), dependencies)


@pytest.fixture(scope="function")
def mock_no_dependencies(monkeypatch):
    mock_changelog(monkeypatch, {}, {})


@pytest.fixture(scope="function")
def changelogs(tmp_path) -> Changelogs:
    changes_path = tmp_path / "doc/changes"
    changes_path.mkdir(parents=True)
    return Changelogs(
        changes_path=changes_path,
        root_path=tmp_path,
        version=Version(major=1, minor=0, patch=0),
    )


class TestChangelogs:
    """
    As some methods in the class `Changelogs` modify files, it is required that the
    fixtures which create the sample files (changelog.md, unreleased.md, & changes_1.0.0.md)
    reset per function and use `tmp_path`. By doing this, we ensure that the sample
    are in their expected state for each test.
    """

    @staticmethod
    def test_create_new_unreleased(changelogs):
        changelogs._create_new_unreleased()

        assert changelogs.unreleased_md.read_text() == UNRELEASED_INITIAL_CONTENT

    @staticmethod
    def test_create_versioned_changelog(changelogs, mock_dependencies):
        changelogs._create_versioned_changelog(SampleContent.changelog)
        saved_text = changelogs.versioned_changelog_md.read_text()

        assert "1.0.0" in saved_text
        assert SampleContent.changelog in saved_text

    @staticmethod
    def test_extract_unreleased_notes(changelogs, unreleased_md):
        actual = changelogs._extract_unreleased_notes()
        expected = "## Summary\n" + SampleContent.changelog + "\n"
        assert actual == expected

    @staticmethod
    def test_dependency_changes(changelogs, mock_dependencies):
        result = changelogs._dependency_changes()
        assert result == (
            "\n"
            "### `main`\n\n"
            "* Updated dependency `package1:0.0.1` to `0.1.0`\n"
            "\n"
            "### `dev`\n\n"
            "* Added dependency `package2:0.2.0`\n"
        )

    @staticmethod
    def test_dependency_changes_without_latest_version(
        changelogs, mock_new_dependencies
    ):
        result = changelogs._dependency_changes()
        assert result == (
            "\n"
            "### `main`\n\n"
            "* Added dependency `package1:0.1.0`\n"
            "\n"
            "### `dev`\n\n"
            "* Added dependency `package2:0.2.0`\n"
        )

    @staticmethod
    @pytest.mark.parametrize(
        "groups,expected",
        [
            pytest.param(
                {"dev", "abcd", "main"}, ["main", "abcd", "dev"], id="with_main"
            ),
            pytest.param(
                {"dev", "abcd", "bacd"}, ["abcd", "bacd", "dev"], id="without_main"
            ),
        ],
    )
    def test_sort_groups(changelogs, groups, expected):
        result = changelogs._sort_groups(groups)
        assert result == expected

    @staticmethod
    def test_update_table_of_contents(changelogs, changes_md):
        changelogs._update_table_of_contents()

        assert changelogs.changelog_md.read_text() == SampleContent.altered_changes

    @staticmethod
    def test_prepare_release(changelogs, mock_dependencies, unreleased_md, changes_md):
        changelogs.prepare_release()
        assert changelogs.changelog_md.read_text() == SampleContent.altered_changes
        assert changelogs.unreleased_md.read_text() == UNRELEASED_INITIAL_CONTENT
        versioned = changelogs.versioned_changelog_md.read_text()
        assert versioned == expected_changes_file_content(with_dependencies=True)

    @staticmethod
    def test_update_latest(
        monkeypatch,
        mock_no_dependencies,
        previous_dependencies,
        dependencies,
        changelogs,
        unreleased_md,
        changes_md,
    ):
        changelogs.prepare_release()
        mock_changelog(monkeypatch, previous_dependencies, dependencies)
        changelogs.update_latest()
        versioned = changelogs.versioned_changelog_md.read_text()
        assert versioned == expected_changes_file_content(with_dependencies=True)

    @staticmethod
    def test_prepare_release_with_no_dependencies(
        changelogs, mock_no_dependencies, unreleased_md, changes_md
    ):
        changelogs.prepare_release()

        assert changelogs.changelog_md.read_text() == SampleContent.altered_changes
        assert changelogs.unreleased_md.read_text() == UNRELEASED_INITIAL_CONTENT
        versioned = changelogs.versioned_changelog_md.read_text()
        assert versioned == expected_changes_file_content()
