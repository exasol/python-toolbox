from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Optional

import tomlkit
from pydantic import (
    BaseModel,
    model_validator,
)
from tomlkit import TOMLDocument

from exasol.toolbox.util.dependencies.shared_models import Package


class PoetryGroup(BaseModel):
    name: str
    toml_section: Optional[str]

    class Config:
        frozen = True


TRANSITIVE_GROUP = PoetryGroup(name="transitive", toml_section=None)


class PoetryDependency(Package):
    name: str
    version: str
    group: PoetryGroup


class PoetryToml(BaseModel):
    working_directory: Path

    @model_validator(mode="before")
    def read_content(cls, values):
        file_path = values["working_directory"] / "pyproject.toml"
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        try:
            text = file_path.read_text()
            cls._content: TOMLDocument = tomlkit.loads(text)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
        return values

    def get_section_dict(self, section: str) -> Optional[dict]:
        current = self._content.copy()
        for section in section.split("."):
            if section not in current:
                return None
            current = current[section]  # type: ignore
        return current

    @property
    def groups(self) -> tuple[PoetryGroup, ...]:
        groups = []

        main_key = "project.dependencies"
        if self.get_section_dict(main_key):
            groups.append(PoetryGroup(name="main", toml_section=main_key))

        main_dynamic_key = "tool.poetry.dependencies"
        if self.get_section_dict(main_dynamic_key):
            groups.append(PoetryGroup(name="main", toml_section=main_dynamic_key))

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


class PoetryDependencies(BaseModel):
    groups: tuple[PoetryGroup, ...]
    working_directory: Path

    @staticmethod
    def _extract_from_line(line: str, group: PoetryGroup) -> PoetryDependency:
        pattern = r"\s+(\d+(?:\.\d+)*)\s+"
        match = re.split(pattern, line)
        return PoetryDependency(name=match[0], version=match[1], group=group)

    def _extract_from_poetry_show(
        self, output_text: str, group: PoetryGroup
    ) -> list[PoetryDependency]:
        return [
            self._extract_from_line(line, group=group)
            for line in output_text.splitlines()
        ]

    @property
    def direct_dependencies(self) -> dict[str, list[PoetryDependency]]:
        dependencies = {}
        for group in self.groups:
            command = ("poetry", "show", "--top-level", f"--only={group.name}")
            output = subprocess.run(
                command, capture_output=True, text=True, cwd=self.working_directory
            )
            result = self._extract_from_poetry_show(
                output_text=output.stdout, group=group
            )
            dependencies[group.name] = result
        return dependencies

    @property
    def all_dependencies(self) -> dict[str, list[PoetryDependency]]:
        command = ("poetry", "show")
        output = subprocess.run(
            command, capture_output=True, text=True, cwd=self.working_directory
        )

        direct_dependencies = self.direct_dependencies.copy()
        transitive_dependencies = []
        names_direct_dependencies = {
            dep.name
            for group_list in direct_dependencies.values()
            for dep in group_list
        }
        for line in output.stdout.splitlines():
            dep = self._extract_from_line(line=line, group=TRANSITIVE_GROUP)
            if dep.name not in names_direct_dependencies:
                transitive_dependencies.append(dep)

        return direct_dependencies | {TRANSITIVE_GROUP.name: transitive_dependencies}
