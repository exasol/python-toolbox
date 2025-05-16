from __future__ import annotations

import shutil
import subprocess
import sys
from urllib import request
import urllib.error
import webbrowser
from itertools import repeat
from pathlib import Path
from typing import (
    Container,
    Iterable,
    Optional,
    Tuple,
)


import nox
from nox import Session

from exasol.toolbox.nox._shared import DOCS_OUTPUT_DIR
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)


def _build_docs(session: nox.Session, config: Config) -> None:
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-W",
        "-b",
        "html",
        f"{config.doc}",
        DOCS_OUTPUT_DIR,
    )


def _build_multiversion_docs(session: nox.Session, config: Config) -> None:
    session.run(
        "poetry",
        "run",
        "sphinx-multiversion",
        f"{config.doc}",
        DOCS_OUTPUT_DIR,
    )
    session.run("touch", f"{DOCS_OUTPUT_DIR}/.nojekyll")


def _doc_files(root: Path) -> Iterable[Path]:
    """Returns an iterator over all documentation files of the project"""
    docs = Path(root).glob("**/*.rst")

    def _deny_filter(path: Path) -> bool:
        return not ("venv" in path.parts)

    return filter(lambda path: _deny_filter(path), docs)


def _doc_urls(files: Iterable[Path]) -> Iterable[tuple[Path, str]]:
    """Returns an iterable over all urls contained in the provided files"""
    def should_filter(url: str) -> bool:
        _filtered: Container[str] = []
        return url.startswith("mailto") or url in _filtered

    for file in files:
        cmd = ["python", "-m", "urlscan", "-n", f"{file}"]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            stderr = result.stderr.decode("utf8")
            msg = f"Could not retrieve url's from file: {file}, details: {stderr}"
            raise Exception(msg)
        stdout = result.stdout.decode("utf8").strip()
        _urls = (url.strip() for url in stdout.split("\n"))
        _urls = (url for url in _urls if url)  # filter empty strings and none
        yield from zip(repeat(file), filter(lambda url: not should_filter(url), _urls))


def _doc_links_check(url: str) -> Tuple[Optional[int], str]:
    """Checks if an url is still working (can be accessed)"""
    try:
        # User-Agent needs to be faked otherwise some webpages will deny access with a 403
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/10.0"})
        result = request.urlopen(req)
        return result.code, f"{result.msg}"
    except urllib.error.HTTPError as ex:
        return ex.code, f"{ex}"


def _git_diff_changes_main() -> int:
    """
    Check if doc/changes is changed and return the exit code of command git diff.
    The exit code is 0 if there are no changes.
    """
    p = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            "origin/main",
            "--",
            PROJECT_CONFIG.root / "doc/changes",
        ],
        capture_output=True,
    )
    return p.returncode


@nox.session(name="docs:multiversion", python=False)
def build_multiversion(session: Session) -> None:
    """Builds the multiversion project documentation"""
    _build_multiversion_docs(session, PROJECT_CONFIG)


@nox.session(name="docs:build", python=False)
def build_docs(session: Session) -> None:
    """Builds the project documentation"""
    _build_docs(session, PROJECT_CONFIG)


@nox.session(name="docs:open", python=False)
def open_docs(session: Session) -> None:
    """Opens the built project documentation"""
    docs_folder = PROJECT_CONFIG.root / DOCS_OUTPUT_DIR
    if not docs_folder.exists():
        session.error(f"No documentation could be found. {docs_folder} is missing")
    index = docs_folder / "index.html"
    webbrowser.open_new_tab(index.as_uri())


@nox.session(name="docs:clean", python=False)
def clean_docs(_session: Session) -> None:
    """Removes the documentations build folder"""
    docs_folder = PROJECT_CONFIG.root / DOCS_OUTPUT_DIR
    if docs_folder.exists():
        shutil.rmtree(docs_folder)


@nox.session(name="docs:links", python=False)
def docs_list_links(session: Session) -> None:
    """List all the links within the documentation."""
    for path, url in _doc_urls(_doc_files(PROJECT_CONFIG.root)):
        session.log(f"Url: {url}, File: {path}")


@nox.session(name="docs:links:check", python=False)
def docs_links_check(session: Session) -> None:
    """Checks whether all links in the documentation are accessible."""
    errors = []
    for path, url in _doc_urls(_doc_files(PROJECT_CONFIG.root)):
        status, details = _doc_links_check(url)
        if status != 200:
            errors.append((path, url, status, details))

    if errors:
        session.error(
            "\n"
            + "\n".join(f"Url: {e[1]}, File: {e[0]}, Error: {e[3]}" for e in errors)
        )


@nox.session(name="changelog:updated", python=False)
def updated(_session: Session) -> None:
    """Checks if the change log has been updated"""
    if _git_diff_changes_main() == 0:
        print(
            "Changelog is not updated.\n"
            "Please describe your changes in the changelog!"
        )
        sys.exit(1)
