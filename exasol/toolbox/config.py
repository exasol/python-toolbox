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
        default=(
            "3.9",
            "3.10",
            "3.11",
            "3.12",
            "3.13",
        ),
        description="Python versions to use in running CI workflows",
    )

    exasol_versions: tuple[ValidVersionStr, ...] = Field(
        default=("7.1.9",),
        description="Exasol versions to use in running CI workflows for integration tests using the DB",
    )
    create_major_version_tags: bool = Field(
        default=False,
        description="If true, creates also the major version tags (v*) automatically",
    )
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @computed_field  # type: ignore[misc]
    @property
    def min_py_version(self) -> str:
        """
        Minimum Python version declared from the `python_versions` list

        This is used in specific testing scenarios where it would be either
        costly to run the tests for all `python_versions` or we need a single metric.
        """
        return str(min([Version.from_string(v) for v in self.python_versions]))
