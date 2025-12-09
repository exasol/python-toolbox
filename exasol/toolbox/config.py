import inspect
from typing import (
    Annotated,
    Any,
)

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
)

from exasol.toolbox.nox.plugin import (
    METHODS_SPECIFIED_FOR_HOOKS,
    PLUGIN_ATTR_NAME,
)
from exasol.toolbox.util.version import Version


def validate_plugin_hook(plugin_class: type[Any]):
    """
    Checks methods in a class for at least one specific pluggy @hookimpl marker
    and verifies that this method is also specified in
    `exasol.toolbox.nox.plugins.NoxTasks`.
    """
    has_hook_implementation = False
    not_specified_decorated_methods = []
    for name, method in inspect.getmembers(plugin_class, inspect.isroutine):
        if hasattr(method, PLUGIN_ATTR_NAME):
            has_hook_implementation = True
            if name not in METHODS_SPECIFIED_FOR_HOOKS:
                not_specified_decorated_methods.append(name)

    if not has_hook_implementation:
        raise ValueError(
            f"No methods in `{plugin_class.__name__}` were found to be decorated"
            "with `@hookimpl`. The `@hookimpl` decorator indicates that this"
            "will be used with pluggy and used in specific nox sessions."
            "Without it, this class does not modify any nox sessions."
        )

    if not_specified_decorated_methods:
        raise ValueError(
            f"{len(not_specified_decorated_methods)} method(s) were "
            "decorated with `@hookimpl`, but these methods were not "
            "specified in `exasol.toolbox.nox.plugins.NoxTasks`: "
            f"{not_specified_decorated_methods}. The `@hookimpl` decorator indicates "
            "that these methods will be used by pluggy to modify specific nox sessions."
            "If the method was not previously specified, then no nox sessions will"
            "be modified. The `@hookimpl` is only used by nox sessions provided by the"
            "pyexasol-toolbox and not ones created for just your project."
        )

    return plugin_class


def valid_version_string(version_string: str) -> str:
    Version.from_string(version_string)
    return version_string


ValidPluginHook = Annotated[type[Any], AfterValidator(validate_plugin_hook)]
ValidVersionStr = Annotated[str, AfterValidator(valid_version_string)]

DEFAULT_EXCLUDED_PATHS = {
    ".eggs",
    ".html-documentation",
    ".poetry",
    ".sonar",
    ".venv",
    "dist",
    "venv",
}


class BaseConfig(BaseModel):
    """
    Basic configuration for projects using the PTB

    This configuration class defines the necessary attributes for using the PTB's
    various nox sessions and GitHub CI workflows. Defaults are provided via the
    attributes, which makes it easy for a specific project to modify these values
    as needed. There are properties provided which automate some configuration aspects
    so that the project-specific modifications are reduced.

    pydantic has been used so that altered attributes are quickly validated.
    This allows for immediate feedback, instead of waiting for various failed CI
    runs.
    """

    python_versions: tuple[ValidVersionStr, ...] = Field(
        default=("3.10", "3.11", "3.12", "3.13", "3.14"),
        description="Python versions to use in running CI workflows",
    )

    exasol_versions: tuple[ValidVersionStr, ...] = Field(
        default=("7.1.30", "8.29.6", "2025.1.0"),
        description="Exasol versions to use in running CI workflows for integration tests using the DB",
    )
    create_major_version_tags: bool = Field(
        default=False,
        description="If true, creates also the major version tags (v*) automatically",
    )
    add_to_excluded_python_paths: tuple[str, ...] = Field(
        default=(),
        description="""
        This is used to extend the default excluded_python_paths. If a more general
        path that would be seen in other projects, like .venv, needs to be added into
        this argument, please instead modify the
        `exasol.toolbox.config.DEFAULT_EXCLUDED_PATHS`.
        """,
    )
    plugins_for_nox_sessions: tuple[ValidPluginHook, ...] = Field(
        default=(),
        description="""
        This is used to provide hooks to extend one or more of the Nox sessions provided
        by the python-toolbox. As described on the plugins pages:
            - https://exasol.github.io/python-toolbox/main/user_guide/customization.html#plugins
            - https://exasol.github.io/python-toolbox/main/developer_guide/plugins.html,
        possible plugin options are defined in `exasol.toolbox.nox.plugins.NoxTasks`.
        """,
    )
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @computed_field  # type: ignore[misc]
    @property
    def minimum_python_version(self) -> str:
        """
        Minimum Python version declared from the `python_versions` list

        This is used in specific testing scenarios where it would be either
        costly to run the tests for all `python_versions` or we need a single metric.
        """
        versioned = [Version.from_string(v) for v in self.python_versions]
        min_version = min(versioned)
        index_min_version = versioned.index(min_version)
        return self.python_versions[index_min_version]

    @computed_field  # type: ignore[misc]
    @property
    def excluded_python_paths(self) -> tuple[str, ...]:
        """
        There are certain nox sessions:
          - format:check
          - format:fix
          - lint:code
          - lint:security
          - lint:typing
        where it is desired to restrict which Python files are considered within the
        PROJECT_CONFIG.source path, like excluding `dist`, `.eggs`. As such, this
        property is used to exclude such undesired paths.
        """
        return tuple(
            DEFAULT_EXCLUDED_PATHS.union(set(self.add_to_excluded_python_paths))
        )

    @computed_field  # type: ignore[misc]
    @property
    def pyupgrade_argument(self) -> tuple[str, ...]:
        """
        Default argument to :func:`exasol.toolbox._format._pyupgrade`.

        It uses the minimum Python version to ensure compatibility with all supported
        versions of a project.
        """
        version_parts = self.minimum_python_version.split(".")[:2]
        version_number = "".join(version_parts)
        return (f"--py{version_number}-plus",)
