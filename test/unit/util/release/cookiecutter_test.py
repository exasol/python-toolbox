from inspect import cleandoc
from json import loads
from pathlib import Path

import pytest

from exasol.toolbox.util.release.cookiecutter import update_cookiecutter_default
from exasol.toolbox.util.version import Version


@pytest.fixture
def cookiecutter_json(tmp_path: Path) -> Path:
    cookiecutter_json = tmp_path / "cookiecutter.json"
    contents = """
    {
      "project_name": "Yet Another Project",
      "repo_name": "{{cookiecutter.project_name | lower | replace(' ', '-')}}",
      "package_name": "{{cookiecutter.repo_name | replace('-', '_')}}",
      "pypi_package_name": "exasol-{{cookiecutter.repo_name}}",
      "import_package": "exasol.{{cookiecutter.package_name}}",
      "description": "",
      "author_full_name": "Exasol AG",
      "author_email": "opensource@exasol.com",
      "project_short_tag": "",
      "python_version_min": "3.10",
      "exasol_toolbox_version_range": ">=4.0.1,<5",
      "license_year": "{% now 'utc', '%Y' %}",
      "__repo_name_slug": "{{cookiecutter.package_name}}",
      "__package_name_slug": "{{cookiecutter.package_name}}",
      "_extensions": [
        "cookiecutter.extensions.TimeExtension"
      ]
    }
    """
    cookiecutter_json.write_text(cleandoc(contents))
    return cookiecutter_json


@pytest.mark.parametrize(
    "version,expected",
    [
        pytest.param(Version(major=5, minor=0, patch=7), ">=5.0.7,<6"),
        pytest.param(Version(major=6, minor=2, patch=7), ">=6.2.7,<7"),
    ],
)
def test_update_cookiecutter_default(
    cookiecutter_json, version: Version, expected: str
):
    update_cookiecutter_default(cookiecutter_json=cookiecutter_json, version=version)

    updated_json = cookiecutter_json.read_text()
    updated_dict = loads(updated_json)
    assert updated_dict["exasol_toolbox_version_range"] == expected
