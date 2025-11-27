from typing import (
    Annotated,
)

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
)

from exasol.toolbox.util.version import Version


def valid_version_string(version_string: str) -> str:
    Version.from_string(version_string)
    return version_string


ValidVersionStr = Annotated[str, AfterValidator(valid_version_string)]


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
        :meth:`exasol.toolbox.config.BaseConfig.excluded_paths` attribute.
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

    @computed_field
    @property
    def excluded_python_paths(self) -> tuple[str, ...]:
        """
        There are certain nox sessions:
          - lint:code
          - lint:security
          - lint:typing
          - project:fix
          - project:format
        where it is desired restrict which Python files are considered within the
        source_path, like excluding `dist`, `.eggs`. As such, this property is used to
        exclude such undesired paths.
        """
        default_excluded_paths = {
            "dist",
            ".eggs",
            "venv",
            ".poetry",
            ".sonar",
            ".html-documentation",
        }
        return tuple(
            default_excluded_paths.union(set(self.add_to_excluded_python_paths))
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
