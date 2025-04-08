from __future__ import annotations

import argparse
import re
import subprocess
import sys
from enum import Enum
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
        usage="nox -s release:experimental -- [-h] [-v | --version VERSION] [-t | --type {major,minor,patch}]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-v",
        "--version",
        type=cli.version,
        help="A version string of the following format:" '"NUMBER.NUMBER.NUMBER"',
        required=False,
        default=argparse.SUPPRESS,
    )
    group.add_argument(
        "-t",
        "--type",
        type=ReleaseTypes,
        help="specifies which type of upgrade is to be performed",
        required=False,
        choices=[rt.value for rt in list(ReleaseTypes)],
        default=argparse.SUPPRESS,
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


class ReleaseTypes(Enum):
    Major = "major"
    Minor = "minor"
    Patch = "patch"


def _type_release(release_type: ReleaseTypes, old_version: Version) -> Version:
    upgrade = {
        ReleaseTypes.Major: Version(old_version.major + 1, 0, 0),
        ReleaseTypes.Minor: Version(old_version.major, old_version.minor + 1, 0),
        ReleaseTypes.Patch: Version(
            old_version.major, old_version.minor, old_version.patch + 1
        ),
    }
    return upgrade[release_type]


def _version_control(
    session: Session,
    args: argparse.Namespace,
) -> Version:
    has_release_version = hasattr(args, "version")
    has_release_type = hasattr(args, "type")

    old_version = Version.from_poetry()

    if has_release_version and not has_release_type:
        if not _is_valid_version(old=old_version, new=args.version):
            session.error(
                f"Invalid version: the release version ({args.version}) "
                f"must be greater than or equal to the current version ({args.version})"
            )
        return args.version

    if not has_release_version and has_release_type:
        return _type_release(release_type=args.type, old_version=old_version)

    session.error("version not allowed with type")


class ReleaseError(Exception):
    """Error during trigger release"""


def _trigger_release() -> Version:
    def run(*args: str):
        try:
            return subprocess.run(
                args, capture_output=True, text=True, check=True
            ).stdout
        except subprocess.CalledProcessError as ex:
            raise ReleaseError(f"failed to execute command {args}") from ex

    branches = run("git", "remote", "show", "origin")
    if not (default_branch := re.search(r"HEAD branch: (\S+)", branches)):
        raise ReleaseError("default branch could not be found")
    default_branch = default_branch.group(1)

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


def _trigger_release_test():
    def run(*args: str):
        return subprocess.run(args, capture_output=True, text=True, check=True).stdout

    v = Version.from_poetry()
    run("echo", "test 1")
    run("echo", "test 2")
    run("echo", "test 3")
    run("echo", "test 4")
    run("echo", "test 5")


@nox.session(name="release:prepare", python=False)
def prepare_release(session: Session, python=False) -> None:
    """
    Prepares the project for a new release.
    """
    parser = _create_parser()
    args = parser.parse_args(session.posargs)

    new_version = _version_control(session, args)
    print(f"release version: {new_version}")

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
    print(_trigger_release())
