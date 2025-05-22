from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import tomlkit
from pydantic import BaseModel, model_validator
from tomlkit import TOMLDocument


class PoetryGroup(BaseModel):
    name: str
    toml_section: str


class PoetryToml(BaseModel):
    file_path: Path = Path("pyproject.toml")
    _content: Optional[TOMLDocument] = None

    @model_validator(mode="before")
    def read_content(cls, values):
        file_path = values["file_path"]
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        try:
            text = file_path.read_text()
            cls._content = tomlkit.loads(text)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
        return values

    def get_section_dict(self, section: str) -> dict | None:
        current = self._content.copy()
        for section in section.split('.'):
            if section not in current:
                return None
            current = current[section]
        return current

    @property
    def groups(self) -> Tuple[PoetryGroup, ...]:
        groups = []

        main_key = "project.dependencies"
        if self.get_section_dict(main_key):
            groups.append(PoetryGroup(name="main", toml_section=main_key))

        # present in some Poetry 2.x pyproject.tomls
        main_dynamic_key = "tool.poetry.dependencies"
        if self.get_section_dict(main_dynamic_key):
            groups.append(
                PoetryGroup(name="main", toml_section=main_dynamic_key)
            )

        group_key = "tool.poetry.group"
        if group_dict := self.get_section_dict(group_key):
            for group, content in group_dict.items():
                if "dependencies" in content:
                    groups.append(
                        PoetryGroup(
                            name=group,
                            toml_section=f"{group_key}.{group}.dependencies",
                        )
                    )
        return tuple(groups)

    # @property
    # def dependencies(self) -> Tuple[Group, ...]:
