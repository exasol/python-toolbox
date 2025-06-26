from __future__ import annotations

from packaging.version import Version
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class Package(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str
    version: Version

    @field_validator("version", mode="before")
    def convert_version(cls, v: str) -> Version:
        return Version(v)

    @property
    def normalized_name(self) -> str:
        return self.name.lower().replace("_", "-")
