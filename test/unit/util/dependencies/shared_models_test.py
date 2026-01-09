import pytest
from packaging.version import Version
from pydantic import BaseModel
from pydantic_core._pydantic_core import ValidationError

from exasol.toolbox.util.dependencies.shared_models import (
    VERSION_TYPE,
    Package,
    PoetryFiles,
    poetry_files_from_latest_tag,
)
from exasol.toolbox.util.git import Git
from noxconfig import PROJECT_CONFIG


class Dummy(BaseModel):
    version: VERSION_TYPE


class TestVersionType:
    @staticmethod
    @pytest.mark.parametrize("input", [1.0, {}])
    def test_wrong_input_raises_error(input):
        with pytest.raises(ValidationError, match="Input should be a valid string"):
            Dummy(version=input)

    @staticmethod
    def test_string_not_version_raises_error():
        with pytest.raises(ValidationError, match="Value error, Invalid version:"):
            Dummy(version="string")

    @staticmethod
    def test_works_as_expected():
        result = Dummy(version="1.0.0")
        assert result.version == Version("1.0.0")


class TestPackage:
    @staticmethod
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("numpy", "numpy"),
            ("sphinxcontrib-applehelp", "sphinxcontrib-applehelp"),
            ("Imaginary_package", "imaginary-package"),
            ("Imaginary_package_2", "imaginary-package-2"),
        ],
    )
    def test_normalized_name(name, expected):
        dep = Package(name=name, version="0.1.0")
        assert dep.normalized_name == expected

    @staticmethod
    def test_coordinates():
        dep = Package(name="numpy", version="0.1.0")
        assert dep.coordinates == "numpy:0.1.0"


def test_poetry_files_from_latest_tag():
    latest_tag = Git.get_latest_tag()
    with poetry_files_from_latest_tag(root_path=PROJECT_CONFIG.root_path) as tmp_dir:
        for file in PoetryFiles().files:
            assert (tmp_dir / file).is_file()

        contents = (tmp_dir / PoetryFiles.pyproject_toml).read_text()
        assert f'version = "{latest_tag}"' in contents
