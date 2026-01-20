from json import (
    dumps,
    loads,
)
from pathlib import Path

from exasol.toolbox.util.version import Version


def update_cookiecutter_default(cookiecutter_json: Path, version: Version) -> None:
    contents = cookiecutter_json.read_text()
    contents_as_dict = loads(contents)

    contents_as_dict["exasol_toolbox_version_range"] = f">={version},<{version.major+1}"

    updated_contents = dumps(contents_as_dict, indent=2)
    cookiecutter_json.write_text(updated_contents)
