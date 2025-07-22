from __future__ import annotations

from typing import (
    Union,
)

from packaging.version import Version
from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.dependencies.shared_models import Package


class DependencyChange(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str


class AddedDependency(DependencyChange):
    version: Version

    def __str__(self) -> str:
        return f"* Added dependency `{self.name}:{self.version}`"

    @classmethod
    def from_package(cls, package: Package) -> AddedDependency:
        return cls(name=package.name, version=package.version)


class RemovedDependency(DependencyChange):
    version: Version

    def __str__(self) -> str:
        return f"* Removed dependency `{self.name}:{self.version}`"

    @classmethod
    def from_package(cls, package: Package) -> RemovedDependency:
        return cls(name=package.name, version=package.version)


class UpdatedDependency(DependencyChange):
    old_version: Version
    current_version: Version

    def __str__(self) -> str:
        return (
            f"* Updated dependency `{self.name}:{self.old_version}` "
            f"to `{self.current_version}`"
        )

    @classmethod
    def from_package(
        cls, old_package: Package, current_package: Package
    ) -> UpdatedDependency:
        return cls(
            name=old_package.name,
            old_version=old_package.version,
            current_version=current_package.version,
        )


class DependencyChanges(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    old_dependencies: dict
    current_dependencies: dict

    def _categorize_change(self, dependency_name: str) -> Union[DependencyChange, None]:
        """
        Categorize dependency change as removed, added, or updated.
        """
        old_dependency = self.old_dependencies.get(dependency_name)
        current_dependency = self.current_dependencies.get(dependency_name)
        if old_dependency and not current_dependency:
            return RemovedDependency.from_package(old_dependency)
        elif not old_dependency and current_dependency:
            return AddedDependency.from_package(current_dependency)
        elif old_dependency.version != current_dependency.version:
            return UpdatedDependency.from_package(old_dependency, current_dependency)
        # dependency was unchanged between versions
        return None

    @property
    def changes(self) -> list[DependencyChange]:
        """
        Return dependency changes
        """
        all_dependencies = sorted(
            self.old_dependencies.keys() | self.current_dependencies.keys()
        )
        return [
            change_dependency
            for dependency_name in all_dependencies
            if (change_dependency := self._categorize_change(dependency_name))
        ]
