from __future__ import annotations

from typing import Optional

from packaging.version import Version
from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.dependencies.shared_models import (
    NormalizedPackageStr,
    Package,
)


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
    previous_version: Version
    current_version: Version

    def __str__(self) -> str:
        return (
            f"* Updated dependency `{self.name}:{self.previous_version}` "
            f"to `{self.current_version}`"
        )

    @classmethod
    def from_package(
        cls, previous_package: Package, current_package: Package
    ) -> UpdatedDependency:
        return cls(
            name=previous_package.name,
            previous_version=previous_package.version,
            current_version=current_package.version,
        )


class DependencyChanges(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    previous_dependencies: dict[NormalizedPackageStr, Package]
    current_dependencies: dict[NormalizedPackageStr, Package]

    def _categorize_change(
        self, dependency_name: NormalizedPackageStr
    ) -> Optional[DependencyChange]:
        """
        Categorize dependency change as removed, added, or updated.
        """
        previous_dependency = self.previous_dependencies.get(dependency_name)
        current_dependency = self.current_dependencies.get(dependency_name)
        if previous_dependency and not current_dependency:
            return RemovedDependency.from_package(previous_dependency)
        elif not previous_dependency and current_dependency:
            return AddedDependency.from_package(current_dependency)
        elif previous_dependency.version != current_dependency.version:  # type: ignore
            return UpdatedDependency.from_package(
                previous_dependency, current_dependency  # type: ignore
            )
        # dependency was unchanged between versions
        return None

    @property
    def changes(self) -> list[DependencyChange]:
        """
        Return dependency changes
        """
        # dict.keys() returns a set converted into a list by `sorted()`
        all_dependencies = sorted(
            self.previous_dependencies.keys() | self.current_dependencies.keys()
        )
        return [
            change_dependency
            for dependency_name in all_dependencies
            if (change_dependency := self._categorize_change(dependency_name))
        ]
