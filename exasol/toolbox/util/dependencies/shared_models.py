from __future__ import annotations

from packaging.version import Version
from pydantic import (
    BaseModel,
    field_validator,
)


class Package(BaseModel):
    name: str
    version: Version

    class Config:
        frozen = True
        arbitrary_types_allowed = True

    @field_validator("version", mode="before")
    def convert_version(cls, v: str) -> Version:
        return Version(v)

    @property
    def normalized_name(self) -> str:
        return self.name.lower().replace("_", "-")
