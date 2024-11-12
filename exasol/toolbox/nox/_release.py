from __future__ import annotations

import argparse
from pathlib import Path
from typing import (
    List,
    Tuple,
)

import nox
from nox import Session

from exasol.toolbox import cli
from exasol.toolbox.nox._shared import (
    Mode,
    _version,
)
from exasol.toolbox.nox.plugin import NoxTasks
from exasol.toolbox.release import (
    Version,
    extract_release_notes,
    new_changelog,
    new_changes,
    new_unreleased,
)
from noxconfig import PROJECT_CONFIG


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nox -s release:prepare",
        usage="nox -s release:prepare -- [-h] version",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "version",
        type=cli.version,
        help=("A version string of the following format:" '"NUMBER.NUMBER.NUMBER"'),
    )
    parser.add_argument(
        "--no-add",
        default=False,
        action="store_true",
        help=("Neither add nor commit the changes"),
    )
    parser.add_argument(
        "--no-branch",
        default=False,
        action="store_true",
        help=("Do not create a branch to commit the changes on"),
    )
    parser.add_argument(
        "--no-pr",
        default=False,
        action="store_true",
        help=("Do not create a pull request for the changes"),
    )
    return parser


def _is_valid_version(old: Version, new: Version) -> bool:
    return new >= old


def _update_project_version(session: Session, version: Version) -> Version:
    session.run("poetry", "version", f"{version}")
    _version(session, Mode.Fix, PROJECT_CONFIG.version_file)
    return version


def _update_changelog(version: Version) -> tuple[Path, Path, Path]:
    unreleased = Path(PROJECT_CONFIG.root) / "doc" / "changes" / "unreleased.md"
    changelog = Path(PROJECT_CONFIG.root) / "doc" / "changes" / f"changes_{version}.md"
    changes = Path(PROJECT_CONFIG.root) / "doc" / "changes" / f"changelog.md"

    changelog_content = extract_release_notes(unreleased)
    changelog.write_text(new_changelog(version, changelog_content))

    unreleased.write_text(new_unreleased())

    changes_content = new_changes(changes, version)
    changes.write_text(changes_content)

    return changelog, changes, unreleased


def _add_files_to_index(session: Session, files: list[Path]) -> None:
    for file in files:
        session.run("git", "add", f"{file}")


@nox.session(name="release:prepare", python=False)
def prepare_release(session: Session, python=False) -> None:
    """
    Prepares the project for a new release.
    """
    parser = _create_parser()
    args = parser.parse_args(session.posargs)

    if not _is_valid_version(
        old=(old_version := Version.from_poetry()),
        new=(new_version := args.version),
    ):
        session.error(
            f"Invalid version: the release version ({new_version}) "
            f"must be greater than or equal to the current version ({old_version})"
        )

    if not args.no_branch and not args.no_add:
        session.run("git", "switch", "-c", f"release/prepare-{new_version}")

    pm = NoxTasks.plugin_manager(PROJECT_CONFIG)

    _ = _update_project_version(session, new_version)
    changelog, changes, unreleased = _update_changelog(new_version)

    pm.hook.prepare_release_update_version(
        session=session, config=PROJECT_CONFIG, version=new_version
    )

    if args.no_add:
        return

    files = [
        changelog,
        unreleased,
        changes,
        PROJECT_CONFIG.root / "pyproject.toml",
        PROJECT_CONFIG.version_file,
    ]
    results = pm.hook.prepare_release_add_files(session=session, config=PROJECT_CONFIG)
    files += [f for plugin_response in results for f in plugin_response]
    _add_files_to_index(
        session,
        files,
    )
    session.run("git", "commit", "-m", f"Prepare release {new_version}")

    if not args.no_pr:
        session.run(
            "gh",
            "pr",
            "create",
            "--title",
            f"Prepare release {new_version}",
            "--body",
            '""',
        )
