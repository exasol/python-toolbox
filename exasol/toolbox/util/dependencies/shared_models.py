from __future__ import annotations

from typing import Annotated

from packaging.version import Version
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
)

VERSION_TYPE = Annotated[str, AfterValidator(lambda v: Version(v))]


class Package(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str
    version: VERSION_TYPE

    @property
    def normalized_name(self) -> str:
        return self.name.lower().replace("_", "-")
