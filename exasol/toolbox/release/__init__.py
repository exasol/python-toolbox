from dataclasses import dataclass


def _index_or(container, index, default):
    try:
        return container[index]
    except IndexError:
        return default


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @staticmethod
    def from_string(version):
        parts = [int(number, base=0) for number in version.split(".")]
        version = [_index_or(parts, i, 0) for i in range(3)]
        return Version(*version)
