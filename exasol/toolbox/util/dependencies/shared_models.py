from __future__ import annotations

import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError
from typing import (
    Annotated,
    Final,
    NewType,
)

from packaging.version import Version
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.git import Git

NormalizedPackageStr = NewType("NormalizedPackageStr", str)

VERSION_TYPE = Annotated[str, AfterValidator(lambda v: Version(v))]


class LatestTagNotFoundError(Exception):
    """Raised when the requested latest tag cannot be found in the repository."""

    def __init__(self, *args):
        super().__init__("The latest git tag was not found in the repository.", *args)


def normalize_package_name(package_name: str) -> NormalizedPackageStr:
    return NormalizedPackageStr(package_name.lower().replace("_", "-"))


def create_package_coordinates(package_name: str, version: str | Version) -> str:
    """
    Create a naming convention for combining a package name and its version
    """
    return f"{package_name}:{version}"


class Package(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str
    version: VERSION_TYPE

    @property
    def coordinates(self) -> str:
        return create_package_coordinates(package_name=self.name, version=self.version)

    @property
    def normalized_name(self) -> NormalizedPackageStr:
        return normalize_package_name(self.name)


@dataclass(frozen=True)
class PoetryFiles:
    pyproject_toml: Final[str] = "pyproject.toml"
    poetry_lock: Final[str] = "poetry.lock"

    @property
    def files(self) -> tuple[str, ...]:
        return tuple(self.__dict__.values())


@contextmanager
def poetry_files_from_latest_tag(root_path: Path) -> Generator[Path]:
    """Context manager to set up a temporary directory with poetry files from the latest tag"""
    try:
        latest_tag = Git.get_latest_tag()
    except CalledProcessError:
        raise LatestTagNotFoundError()

    path = root_path.relative_to(Git.toplevel())
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmp_dir = Path(tmpdir_str)
        for file in PoetryFiles().files:
            Git.checkout(latest_tag, path / file, tmp_dir / file)
        yield tmp_dir
