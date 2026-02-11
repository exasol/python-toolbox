from json import (
    dumps,
    loads,
)
from pathlib import Path

from exasol.toolbox.util.version import Version

PROJECT_ROOT = Path(__file__).resolve().parents[4]
COOKIECUTTER_JSON = PROJECT_ROOT / "project-template" / "cookiecutter.json"


def update_cookiecutter_default(version: Version) -> None:
    contents = COOKIECUTTER_JSON.read_text()
    contents_as_dict = loads(contents)

    contents_as_dict["exasol_toolbox_version_range"] = f">={version},<{version.major+1}"

    updated_contents = dumps(contents_as_dict, indent=2)
    COOKIECUTTER_JSON.write_text(updated_contents)
