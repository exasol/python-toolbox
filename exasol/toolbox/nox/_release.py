from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import (
    Mode,
    _version,
)
from exasol.toolbox.nox.plugin import NoxTasks
from exasol.toolbox.release import (
    extract_release_notes,
    new_changelog,
    new_changes,
    new_unreleased,
)
from exasol.toolbox.util.version import (
    ReleaseTypes,
    Version,
)
from noxconfig import PROJECT_CONFIG


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nox -s release:prepare",
        usage="nox -s release:prepare -- [-h] [-t | --type {major,minor,patch}]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--type",
        type=ReleaseTypes,
        help="specifies which type of upgrade is to be performed",
        required=True,
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--no-add",
        default=False,
        action="store_true",
        help="Neither add nor commit the changes",
    )
    parser.add_argument(
        "--no-branch",
        default=False,
        action="store_true",
        help="Do not create a branch to commit the changes on",
    )
    parser.add_argument(
        "--no-pr",
        default=False,
        action="store_true",
        help="Do not create a pull request for the changes",
    )
    return parser


def _is_valid_version(old: Version, new: Version) -> bool:
    return new >= old


def _update_project_version(session: Session, version: Version) -> Version:
    session.run("poetry", "version", f"{version}")
    _version(session, Mode.Fix)
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


class ReleaseError(Exception):
    """Error during trigger release"""


def _trigger_release() -> Version:
    def run(*args: str):
        try:
            return subprocess.run(
                args, capture_output=True, text=True, check=True
            ).stdout
        except subprocess.CalledProcessError as ex:
            raise ReleaseError(
                f"failed to execute command {ex.cmd}\n\n{ex.stderr}"
            ) from ex

    branches = run("git", "remote", "show", "origin")
    if not (result := re.search(r"HEAD branch: (\S+)", branches)):
        raise ReleaseError("default branch could not be found")
    default_branch = result.group(1)

    run("git", "checkout", default_branch)
    run("git", "pull")

    release_version = Version.from_poetry()
    print(f"release version: {release_version}")

    if re.search(rf"{release_version}", run("git", "tag", "--list")):
        raise ReleaseError(f"tag {release_version} already exists")
    if re.search(rf"{release_version}", run("gh", "release", "list")):
        raise ReleaseError(f"release {release_version} already exists")

    run("git", "tag", str(release_version))
    run("git", "push", "origin", str(release_version))
    return release_version


@nox.session(name="release:prepare", python=False)
def prepare_release(session: Session) -> None:
    """
    Prepares the project for a new release.
    """
    parser = _create_parser()
    args = parser.parse_args(session.posargs)

    new_version = Version.upgrade_version_from_poetry(args.type)

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


@nox.session(name="release:trigger", python=False)
def trigger_release(session: Session) -> None:
    """trigger an automatic project release"""
    print(f"new version: {_trigger_release()}")
