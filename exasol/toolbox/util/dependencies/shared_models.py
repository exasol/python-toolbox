from __future__ import annotations

from typing import (
    Annotated,
    NewType,
)

from packaging.version import Version
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
)

NormalizedPackageStr = NewType("NormalizedPackageStr", str)

VERSION_TYPE = Annotated[str, AfterValidator(lambda v: Version(v))]


def normalize_package_name(package_name: str) -> NormalizedPackageStr:
    return NormalizedPackageStr(package_name.lower().replace("_", "-"))


class Package(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str
    version: VERSION_TYPE

    @property
    def normalized_name(self) -> NormalizedPackageStr:
        return normalize_package_name(self.name)
