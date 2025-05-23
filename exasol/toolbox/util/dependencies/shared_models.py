from __future__ import annotations

from pydantic import BaseModel


class Package(BaseModel):
    name: str
    version: str

    class Config:
        frozen = True

    @property
    def normalized_name(self) -> str:
        return self.name.lower().replace("_", "-")
