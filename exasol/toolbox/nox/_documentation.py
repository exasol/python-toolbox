from __future__ import annotations

import shutil
import webbrowser

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
