from dataclasses import dataclass


@dataclass(frozen=True)
class Version:
    major : int
    minor : int
    patch : int


    @staticmethod
    def from_string(version):
        return Version(0,0,0)
