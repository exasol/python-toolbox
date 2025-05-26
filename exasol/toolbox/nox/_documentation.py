from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
from requests import (
    get,
    head,
)
from requests.exceptions import Timeout

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
    ignore = [r".*"]
    env = os.environ.copy()
    env["SPHINX_EXTRA_LINKCHECK_IGNORES"] = ",".join(ignore)
    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        sp = subprocess.run(
            [
                "poetry",
                "run",
                "--",
                "sphinx-build",
                "-b",
                "linkcheck",
                PROJECT_CONFIG.root / "doc",
                tmpdir,
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        print(sp.returncode)
        if sp.returncode >= 2:
            print(sp.stderr)
            session.error(2)
        output = tmpdir / "output.json"
        links = output.read_text().split("\n")
        file_links = []
        for link in links:
            if link != "":
                line = json.loads(link)
                if not line["uri"].startswith("#"):
                    file_links.append(line)
        file_links.sort(key=lambda file: file["filename"])
        print(
            "\n".join(
                f"filename: {fl['filename']} -> uri: {fl['uri']}" for fl in file_links
            )
        )


@nox.session(name="docs:links:check", python=False)
def docs_links_check(session: Session) -> None:
    """Checks whether all links in the documentation are accessible."""
    ignore = [r"https?://"]
    env = os.environ.copy()
    env["SPHINX_EXTRA_LINKCHECK_IGNORES"] = ",".join(ignore)
    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        sp = subprocess.run(
            [
                "poetry",
                "run",
                "--",
                "sphinx-build",
                "-b",
                "linkcheck",
                PROJECT_CONFIG.root / "doc",
                tmpdir,
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        print(sp.returncode)
        if sp.returncode >= 2:
            print(sp.stderr)
            session.error(2)
        output = tmpdir / "output.json"
        results = output.read_text().split("\n")
        reslen = len(results)
        resstr = results[-1]
        if (reslen == 0) or ((reslen == 1) and (resstr == "")):
            return
        elif resstr == "":
            results.pop()
        for line_nr, result in enumerate(results):
            resdict = json.loads(result)
            if resdict["status"] == "ignored" and resdict["uri"].startswith("http"):
                try:
                    match = re.search(r"https?://[^\s\"\'<>]+", resdict["uri"])
                    if match:
                        resdict["uri"] = match.group()
                    print(f"{line_nr}/{reslen}")
                    request = head(resdict["uri"], timeout=5)
                    if request.status_code != 200:
                        request = get(resdict["uri"], timeout=5, stream=True)
                        request.close()
                    if request.status_code >= 400:
                        resdict["status"] = "broken"
                        resdict["code"] = request.status_code
                    if request.status_code < 400:
                        resdict["status"] = "working"
                        resdict["code"] = request.status_code
                except Timeout:
                    resdict["status"] = "timeout"
                results[line_nr] = json.dumps(resdict)
        output.write_text("\n".join(f"{r}" for r in results))
        errors = []
        for result in results:
            data = json.loads(result)
            if (data["status"] == "broken") or data["status"] == "timeout":
                errors.append(result)
        if errors:
            print("Error" + "s" if len(errors) > 1 else "")
            print("\n".join(error for error in errors))
            session.error(1)


@nox.session(name="changelog:updated", python=False)
def updated(_session: Session) -> None:
    """Checks if the change log has been updated"""
    if _git_diff_changes_main() == 0:
        print(
            "Changelog is not updated.\n"
            "Please describe your changes in the changelog!"
        )
        sys.exit(1)
