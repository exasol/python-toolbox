from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DOC = PROJECT_ROOT / "doc"
DOC_BUILD = DOC / "build"
VERSION_FILE = PROJECT_ROOT / "exasol" / "toolbox" / "version.py"
MIN_CODE_COVERAGE = 10
