from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Annotated,
    Optional,
)

from pydantic import (
    AfterValidator,
    BaseModel,
    computed_field,
    ConfigDict
)
from pydantic.dataclasses import dataclass

from exasol.toolbox.util.version import Version


def str_like_version_validation(versions: list[str]):
    for version in versions:
        Version.from_string(version)
    return versions


class BaseConfig(BaseModel):
    """
    Basic Configuration for Projects

    Attributes:
        * python_versions (Iterable[str]): Iterable over all available python versions of the project [default: ("3.9", "3.10", "3.11", "3.12", "3.13")]
        * min_py_version : Minimum of python_versions
        * max_py_version: Maximum of python_versions
        * exasol_versions: (Iterable[str]): Iterabble over all available exasol versions [default: ("7.1.9)
    """

    python_versions: Annotated[
        list[str], AfterValidator(str_like_version_validation)
    ] = ["3.9", "3.10", "3.11", "3.12", "3.13"]
    exasol_versions: Annotated[
        list[str], AfterValidator(str_like_version_validation)
    ] = ["7.1.9"]
    model_config = ConfigDict(frozen=True)

    @computed_field
    @property
    def min_py_version(self) -> str:
        return str(min([Version.from_string(v) for v in self.python_versions]))

    @computed_field
    @property
    def max_py_version(self) -> str:
        return str(max([Version.from_string(v) for v in self.python_versions]))
