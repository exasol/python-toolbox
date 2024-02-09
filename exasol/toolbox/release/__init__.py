from dataclasses import dataclass
from functools import total_ordering


def _index_or(container, index, default):
    try:
        return container[index]
    except IndexError:
        return default


@total_ordering
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    def __lt__(self, other):
        return (
            self.major < other.major
            or (self.major <= other.major and self.minor < other.minor)
            or (
                self.major <= other.major
                and self.minor <= other.minor
                and self.patch < other.patch
            )
        )

    def __eq__(self, other):
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    @staticmethod
    def from_string(version):
        parts = [int(number, base=0) for number in version.split(".")]
        version = [_index_or(parts, i, 0) for i in range(3)]
        return Version(*version)
