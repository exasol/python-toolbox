from __future__ import annotations

import nox
from nox import Session

from noxconfig import PROJECT_CONFIG


@nox.session(name="package:check", python=False)
def package_check(session: Session) -> None:
    """Checks whether your distribution’s long description will render correctly on PyPI

    This has more robust checks for rst documentation than markdown.
    """
    session.run("poetry", "build", "--project", PROJECT_CONFIG.root_path)
    session.run("twine", "check", PROJECT_CONFIG.root_path / "./dist/*")
