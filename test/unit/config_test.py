from pathlib import Path

import pytest
from pydantic_core._pydantic_core import ValidationError

from exasol.toolbox.config import (
    DEFAULT_EXCLUDED_PATHS,
    BaseConfig,
    valid_version_string,
)
from exasol.toolbox.nox.plugin import hookimpl
from exasol.toolbox.util.version import Version


class TestBaseConfig:
    @staticmethod
    def test_works_as_defined(test_project_config_factory):
        config = test_project_config_factory()

        root_path = config.root_path
        assert config.model_dump() == {
            "add_to_excluded_python_paths": (),
            "create_major_version_tags": False,
            "dependency_manager": {"name": "poetry", "version": "2.3.0"},
            "documentation_path": root_path / "doc",
            "exasol_versions": ("7.1.30", "8.29.13", "2025.1.8"),
            "excluded_python_paths": (
                ".eggs",
                ".html-documentation",
                ".poetry",
                ".sonar",
                ".venv",
                "dist",
                "venv",
            ),
            "github_template_dict": {
                "dependency_manager_version": "2.3.0",
                "minimum_python_version": "3.10",
                "os_version": "ubuntu-24.04",
            },
            "minimum_python_version": "3.10",
            "os_version": "ubuntu-24.04",
            "plugins_for_nox_sessions": (),
            "project_name": "test",
            "python_versions": ("3.10", "3.11", "3.12", "3.13", "3.14"),
            "pyupgrade_argument": ("--py310-plus",),
            "root_path": root_path,
            "sonar_code_path": Path("exasol/test"),
            "source_code_path": root_path / "exasol" / "test",
            "version_filepath": root_path / "exasol" / "test" / "version.py",
        }

    @staticmethod
    @pytest.mark.parametrize(
        "wrong_input,expected_message",
        [
            pytest.param(
                {"python_versions": ["1.2.3.1"]},
                "Version has an invalid format",
                id="python_versions",
            ),
            pytest.param(
                {"exasol_versions": ["1.2.3.1"]},
                "Version has an invalid format",
                id="exasol_versions",
            ),
        ],
    )
    def test_raises_exception_when_incorrect_modification(
        wrong_input: dict, expected_message: str
    ):
        with pytest.raises(ValidationError, match=expected_message):
            BaseConfig(**wrong_input)


class TestValidVersionString:
    @staticmethod
    def test_work_as_expected():
        version_string = "1.2.3"
        result = valid_version_string(version_string=version_string)
        assert result == version_string

    @staticmethod
    def test_raises_exception_when_not_valid():
        with pytest.raises(ValueError):
            valid_version_string("$.2.3")


class BaseConfigExpansion(BaseConfig):
    expansion1: str = "test1"


def test_expansion_validation_fails_for_invalid_version():
    with pytest.raises(ValueError):
        BaseConfigExpansion(python_versions=("1.f.0",))


def test_minimum_python_version(test_project_config_factory):
    conf = test_project_config_factory(python_versions=("5.5.5", "1.10", "9.9.9"))
    assert conf.minimum_python_version == "1.10"


@pytest.mark.parametrize("minimum_python_version", ["3.10", "3.10.5"])
def test_pyupgrade_argument(test_project_config_factory, minimum_python_version):
    conf = test_project_config_factory(
        python_versions=("3.11", minimum_python_version, "3.12")
    )
    assert conf.pyupgrade_argument == ("--py310-plus",)


@pytest.mark.parametrize(
    "add_to_excluded_python_paths,expected",
    [
        pytest.param((), tuple(DEFAULT_EXCLUDED_PATHS), id="no_additions"),
        pytest.param(
            (next(iter(DEFAULT_EXCLUDED_PATHS)),),
            tuple(DEFAULT_EXCLUDED_PATHS),
            id="duplicate_addition",
        ),
        pytest.param(
            ("dummy",), tuple(DEFAULT_EXCLUDED_PATHS) + ("dummy",), id="add_a_new_entry"
        ),
    ],
)
def test_excluded_python_paths(
    test_project_config_factory, add_to_excluded_python_paths, expected
):
    conf = test_project_config_factory(
        add_to_excluded_python_paths=add_to_excluded_python_paths
    )
    assert sorted(conf.excluded_python_paths) == sorted(expected)


class WithHook:
    @hookimpl
    def prepare_release_update_version(self, session, config, version: Version) -> None:
        print("This is a simple, silly hook.")


class WithNotSpecifiedHook:
    @hookimpl
    def not_specified_anywhere(self, session, config, version: Version) -> None:
        print("This is not a properly prepared hook.")


class WithoutHook:
    def prepare_release_update_version(self, session, config, version: Version) -> None:
        print("This is not a properly prepared hook.")


class TestPlugins:
    @staticmethod
    def test_works_when_empty(test_project_config_factory):
        test_project_config_factory(plugins_for_nox_sessions=())

    @staticmethod
    def test_works_for_hook(test_project_config_factory, capsys):
        test_project_config_factory(plugins_for_nox_sessions=(WithHook,))

    @staticmethod
    def test_raises_exception_method_with_hook_not_specified(
        test_project_config_factory,
    ):
        with pytest.raises(ValidationError) as ex:
            test_project_config_factory(
                plugins_for_nox_sessions=(WithNotSpecifiedHook,)
            )
        assert "1 method(s) were decorated with `@hookimpl`, but" in str(ex.value)
        assert "('not_specified_anywhere',)" in str(ex.value)

    @staticmethod
    def test_raises_exception_without_hook(test_project_config_factory):
        with pytest.raises(ValidationError) as ex:
            test_project_config_factory(plugins_for_nox_sessions=(WithoutHook,))
        assert "No methods in `WithoutHook`" in str(ex.value)
