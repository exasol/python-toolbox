from __future__ import annotations

from datetime import datetime
from inspect import cleandoc
from unittest.mock import Mock

import pytest

import exasol.toolbox.util.release.changelog as impl
from exasol.toolbox.util.dependencies.shared_models import LatestTagNotFoundError
from exasol.toolbox.util.release.changelog import (
    UNRELEASED_INITIAL_CONTENT,
    Changelog,
)
from exasol.toolbox.util.release.markdown import Markdown
from exasol.toolbox.util.version import Version


class SampleData:
    def __init__(self, unreleased: str, old_changelog: str, new_changelog: str):
        self.unreleased = Markdown.parse(unreleased).rendered
        self.unreleased_body = "\n".join(self.unreleased.splitlines()[1:])
        self.old_changelog = old_changelog
        self.new_changelog = new_changelog


SAMPLE = SampleData(
    unreleased=cleandoc(
        """
        # Unreleased
        ## Summary
        Summary of changes.

        ## Features
        * Added awesome feature

        ## Bugfixes
        * Fixed nasty bug

        ## Refactorings
        * Some refactoring
        """
    ),
    old_changelog=cleandoc(
        """
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
        """
    ),
    new_changelog=cleandoc(
        """
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
        """
    ),
)


def _markdown(content: str) -> Markdown:
    return Markdown.parse(cleandoc(content))


def expected_changes_file_content(with_dependencies: bool = False) -> Markdown:
    changes = Markdown.parse(SAMPLE.unreleased)
    changes.title = f"# 1.0.0 - {datetime.today().strftime('%Y-%m-%d')}"
    if not with_dependencies:
        return changes

    dependencies = _markdown(
        f"""
        ## Dependency Updates
        ### `main`
        * Updated dependency `package1:0.0.1` to `0.1.0`
        ### `dev`
        * Added dependency `package2:0.2.0`
        """
    )
    return changes.replace_child(dependencies)


@pytest.fixture(scope="function")
def changelog(tmp_path) -> Changelog:
    changes_path = tmp_path / "doc/changes"
    changes_path.mkdir(parents=True)
    return Changelog(
        changes_path=changes_path,
        root_path=tmp_path,
        version=Version(major=1, minor=0, patch=0),
    )


@pytest.fixture(scope="function")
def changes_md(changelog):
    changelog.changelog.write_text(SAMPLE.old_changelog)


@pytest.fixture(scope="function")
def unreleased_md(changelog):
    changelog.unreleased.write_text(SAMPLE.unreleased)


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


class TestChangelogs:
    """
    As some methods in the class `Changelog` modify files, it is required
    that the fixtures which create the sample files (changelog.md,
    unreleased.md, & changes_1.0.0.md) reset per function and use
    `tmp_path`. By doing this, we ensure that the sample are in their expected
    state for each test.
    """

    @staticmethod
    def test_create_new_unreleased(changelog):
        changelog._create_new_unreleased()

        assert changelog.unreleased.read_text() == UNRELEASED_INITIAL_CONTENT

    @staticmethod
    def test_create_versioned_changes(changelog, mock_dependencies):
        changelog._create_versioned_changes(SAMPLE.unreleased)
        saved_text = changelog.versioned_changes.read_text()

        assert "1.0.0" in saved_text
        assert SAMPLE.unreleased_body in saved_text

    @staticmethod
    def test_dependency_changes(changelog, mock_dependencies):
        actual = changelog._dependency_changes()
        expected = _markdown(
            """
            ## Dependency Updates
            ### `main`
            * Updated dependency `package1:0.0.1` to `0.1.0`
            ### `dev`
            * Added dependency `package2:0.2.0`
            """
        )
        assert expected == actual

    @staticmethod
    def test_dependency_changes_without_latest_version(
        changelog, mock_new_dependencies
    ):
        actual = changelog._dependency_changes()
        expected = _markdown(
            """
            ## Dependency Updates
            ### `main`
            * Added dependency `package1:0.1.0`
            ### `dev`
            * Added dependency `package2:0.2.0`
            """
        )
        assert expected == actual

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
    def test_sort_groups(changelog, groups, expected):
        result = changelog._sort_groups(groups)
        assert result == expected

    @staticmethod
    def test_update_table_of_contents(changelog, changes_md):
        changelog._update_table_of_contents()

        assert changelog.changelog.read_text() == SAMPLE.new_changelog

    @staticmethod
    def test_prepare_release(changelog, mock_dependencies, unreleased_md, changes_md):
        changelog.prepare_release()
        assert changelog.changelog.read_text() == SAMPLE.new_changelog
        assert changelog.unreleased.read_text() == UNRELEASED_INITIAL_CONTENT
        versioned = Markdown.read(changelog.versioned_changes)
        assert versioned == expected_changes_file_content(with_dependencies=True)

    @staticmethod
    def test_update_latest(
        monkeypatch,
        mock_no_dependencies,
        previous_dependencies,
        dependencies,
        changelog,
        unreleased_md,
        changes_md,
    ):
        changelog.prepare_release()
        mock_changelog(monkeypatch, previous_dependencies, dependencies)
        changelog.update_latest()
        versioned = Markdown.read(changelog.versioned_changes)
        assert versioned == expected_changes_file_content(with_dependencies=True)

    @staticmethod
    def test_prepare_release_with_no_dependencies(
        changelog, mock_no_dependencies, unreleased_md, changes_md
    ):
        changelog.prepare_release()

        assert changelog.changelog.read_text() == SAMPLE.new_changelog
        assert changelog.unreleased.read_text() == UNRELEASED_INITIAL_CONTENT
        versioned = Markdown.read(changelog.versioned_changes)
        assert versioned == expected_changes_file_content()
