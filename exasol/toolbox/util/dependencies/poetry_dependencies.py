from __future__ import annotations

import subprocess
from collections import OrderedDict
from pathlib import Path

import tomlkit
from pydantic import (
    BaseModel,
    ConfigDict,
)
from tomlkit import TOMLDocument

from exasol.toolbox.util.dependencies.shared_models import (
    NormalizedPackageStr,
    Package,
    PoetryFiles,
    poetry_files_from_latest_tag,
)


class PoetryGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    toml_section: str | None


TRANSITIVE_GROUP = PoetryGroup(name="transitive", toml_section=None)


class PoetryToml(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: TOMLDocument

    @classmethod
    def load_from_toml(cls, working_directory: Path) -> PoetryToml:
        file_path = working_directory / PoetryFiles.pyproject_toml
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        try:
            text = file_path.read_text()
            content = tomlkit.loads(text)
            return cls(content=content)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")

    def get_section_dict(self, section: str) -> dict | None:
        current = self.content.copy()
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


def run_command(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, capture_output=True, text=True, cwd=cwd, check=True
    )  # nosec: B603 - risk of untrusted input for subprocess call is accepted


class PoetryDependencies(BaseModel):
    groups: tuple[PoetryGroup, ...]
    working_directory: Path

    @staticmethod
    def _extract_from_line(line: str) -> Package | None:
        # remove (!) from line as indicates not installed in environment,
        # which could occur for optional dependencies
        split_line = line.replace("(!)", "").strip().split(maxsplit=2)
        if len(split_line) < 2:
            print(f"Unable to parse dependency={line}")
            return None
        return Package(name=split_line[0], version=split_line[1])

    def _extract_from_poetry_show(
        self, output_text: str
    ) -> dict[NormalizedPackageStr, Package]:
        return {
            package.normalized_name: package
            for line in output_text.splitlines()
            if (package := self._extract_from_line(line))
        }

    @property
    def direct_dependencies(
        self,
    ) -> OrderedDict[str, dict[NormalizedPackageStr, Package]]:
        dependencies = OrderedDict()
        for group in self.groups:
            proc = run_command(
                "poetry",
                "show",
                "--top-level",
                f"--only={group.name}",
                "--no-truncate",
                cwd=self.working_directory,
            )
            result = self._extract_from_poetry_show(output_text=proc.stdout)
            dependencies[group.name] = result
        return dependencies

    @property
    def all_dependencies(self) -> OrderedDict[str, dict[NormalizedPackageStr, Package]]:
        proc = run_command(
            "poetry",
            "show",
            "--no-truncate",
            cwd=self.working_directory,
        )
        direct_dependencies = self.direct_dependencies.copy()
        transitive_dependencies = {}
        names_direct_dependencies = {
            package_name
            for group_list in direct_dependencies
            for package_name in group_list
        }
        for line in proc.stdout.splitlines():
            dep = self._extract_from_line(line=line)
            if dep and dep.name not in names_direct_dependencies:
                transitive_dependencies[dep.normalized_name] = dep

        return direct_dependencies | {TRANSITIVE_GROUP.name: transitive_dependencies}


def get_dependencies(
    working_directory: Path,
) -> OrderedDict[str, dict[NormalizedPackageStr, Package]]:
    poetry_dep = PoetryToml.load_from_toml(working_directory=working_directory)
    return PoetryDependencies(
        groups=poetry_dep.groups, working_directory=working_directory
    ).direct_dependencies


def get_dependencies_from_latest_tag() -> (
    OrderedDict[str, dict[NormalizedPackageStr, Package]]
):
    with poetry_files_from_latest_tag() as tmp_dir:
        return get_dependencies(working_directory=tmp_dir)
