from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    build: Path = Path(__file__).parent / "build"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    min_code_coverage = 10
