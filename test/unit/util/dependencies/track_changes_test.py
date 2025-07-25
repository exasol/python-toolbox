from exasol.toolbox.util.dependencies.shared_models import Package
from exasol.toolbox.util.dependencies.track_changes import (
    AddedDependency,
    DependencyChanges,
    RemovedDependency,
    UpdatedDependency,
)


class SamplePackage:
    name = "black"
    version = "25.1.0"

    @property
    def package(self) -> Package:
        return Package(name=self.name, version=self.version)

    @property
    def dependency_dict(self) -> dict[str, Package]:
        return {self.name: self.package}


class TestDependencyChanges:
    @staticmethod
    def test_removed_dependency():
        changes = DependencyChanges(
            previous_dependencies=SamplePackage().dependency_dict,
            current_dependencies={},
        )

        result = changes._categorize_change(SamplePackage.name)

        assert result == RemovedDependency.from_package(SamplePackage().package)
        assert str(result) == "* Removed dependency `black:25.1.0`"

    @staticmethod
    def test_added_dependency():
        changes = DependencyChanges(
            previous_dependencies={},
            current_dependencies=SamplePackage().dependency_dict,
        )

        result = changes._categorize_change(SamplePackage.name)

        assert result == AddedDependency.from_package(SamplePackage().package)
        assert str(result) == "* Added dependency `black:25.1.0`"

    @staticmethod
    def test_updated_dependency():
        old_package = Package(name=SamplePackage.name, version="24.1.0")

        changes = DependencyChanges(
            previous_dependencies={SamplePackage.name: old_package},
            current_dependencies=SamplePackage().dependency_dict,
        )

        result = changes._categorize_change(SamplePackage.name)

        assert result == UpdatedDependency.from_package(
            old_package=old_package, current_package=SamplePackage().package
        )
        assert str(result) == "* Updated dependency `black:24.1.0` to `25.1.0`"

    @staticmethod
    def test_dependency_without_changes():
        changes = DependencyChanges(
            previous_dependencies=SamplePackage().dependency_dict,
            current_dependencies=SamplePackage().dependency_dict,
        )

        result = changes._categorize_change(SamplePackage.name)

        assert result is None

    @staticmethod
    def test_changes_with_no_changed_dependencies():
        changes = DependencyChanges(
            previous_dependencies=SamplePackage().dependency_dict,
            current_dependencies=SamplePackage().dependency_dict,
        )

        assert changes.changes == []

    @staticmethod
    def test_changes_with_changed_dependencies():
        current_dependencies = SamplePackage().dependency_dict.copy()
        added_package = Package(name="pylint", version="3.3.7")
        current_dependencies[added_package.name] = added_package

        changes = DependencyChanges(
            previous_dependencies=SamplePackage().dependency_dict,
            current_dependencies=current_dependencies,
        )

        assert changes.changes == [AddedDependency.from_package(added_package)]
