import sys
from abc import abstractmethod
from typing import Iterable, List
from dataclasses import dataclass


class Dependency:
    @abstractmethod
    def report(self):
        ...


@dataclass(frozen=True)
class AddedDependency(Dependency):
    name: str
    version: str

    def report(self):
        print(f'* Added dependency `{self.name}:{self.version}`')


@dataclass(frozen=True)
class RemovedDependency(Dependency):
    name: str
    version: str

    def report(self):
        print(f'* Removed dependency `{self.name}:{self.version}`')


@dataclass(frozen=True)
class ChangedDependency(Dependency):
    name: str
    old_version: str
    new_version: str

    def report(self):
        print(f'* Updated dependency'
              f' `{self.name}:{self.old_version}`'
              f' to `{self.new_version}`')


class DependencyChanges:
    def __init__(self, heading:str):
        self.heading = heading
        self.dependencies = []
        self.old = {}
        self.new = {}

    @property
    def changes(self) -> Iterable[Dependency]:
        for dep in self.dependencies:
            d0 = self.old.get(dep)
            d1 = self.new.get(dep)
            if d0 and not d1:
                yield RemovedDependency(dep, d0)
            elif not d0 and d1:
                yield AddedDependency(dep, d1)
            elif d0 and d1 and d0 != d1:
                yield ChangedDependency(dep, d0, d1)

    def report(self):
        print(f"\n### {self.heading}\n")
        for c in self.changes:
            c.report()


class DependencyReport:
    def __init__(self, tag:str):
        self.tag = tag
        self.changes: List[DependencyChanges] = []

    def add_changes(self, changes: List[DependencyChanges]):
        self.changes.append(changes)
        return self

    def has_changes(self):
        for c in self.changes:
            if c.changes:
                return True
        return False

    def generate(self):
        if not self.has_changes():
            print(
                f"No dependency updates compared to version {self.tag}.",
                file=sys.stderr,
            )
            return
        print("## Dependency Updates")
        print(f"\nCompared to version {self.tag}"
              " this release updates the following dependencies:")
        for c in self.changes:
            c.report()
