from collections.abc import Mapping
from pathlib import Path


class YamlError(Exception):
    """
    Base exception for YAML errors.
    """

    message_template = "An error occurred with file: {file_path}"

    def __init__(self, file_path: Path, **kwargs):
        self.file_path = file_path
        # Format the template defined in the subclass
        message = self.message_template.format(file_path=file_path, **kwargs)
        super().__init__(message)


class YamlOutputError(YamlError):
    """
    Raised when the final workflow cannot be exported as a YAML file.
    This would likely indicate that one of the preceding transformation steps
    led to a format that is no longer able to be exported as a YAML file.
    """

    message_template = "File {file_path} could not be output by ruamel-yaml."


class YamlParsingError(YamlError):
    """
    Raised when the rendered template is not a valid YAML file, as it cannot be
    parsed by ruamel-yaml.
    """

    message_template = (
        "File {file_path} could not be parsed. Check for invalid YAML syntax."
    )


class TemplateRenderingError(YamlError):
    """
    Raised when Jinja fails to modify the template. It may be that a Jinja
    variable was not defined, a brace was not closed, etc.
    """

    message_template = (
        "File {file_path} failed to render. Check for Jinja-related errors."
    )


class InvalidWorkflowPatcherYamlError(YamlError):
    """
    Raised when the :class:`WorkflowPatcher` failed the validation constraints of
    :class:`WorkflowPatcherConfig`.
    """

    message_template = "File '{file_path}' is malformed; it failed Pydantic validation."


class InvalidWorkflowPatcherEntryError(YamlError):
    """
    Raised when the :class:`WorkflowPatcher` is used but one of the specified keys it
    listed does not exist in the relevant workflow template file.
    """

    message_template = (
        "In file '{file_path}', an entry '{entry}' does not exist in "
        "the workflow template. Please fix the entry."
    )


class YamlKeyError(Exception):
    """
    Base exception for when a specified value cannot be found in a YAML.
    """

    message_template = "An error occurred with job: '{job_name}'"

    def __init__(self, **kwargs):
        # Store all attributes dynamically (job_name, step_id, etc.)
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._data = kwargs
        # Format the template using the passed-in arguments
        super().__init__(self.message_template.format(**kwargs))

    @property
    def entry(self) -> Mapping[str, str]:
        return self._data


class YamlJobValueError(YamlKeyError):
    """
    Raised when a job cannot be found in a YAML file.
    """

    message_template = "Job '{job_name}' could not be found"


class YamlStepIdValueError(YamlKeyError):
    """
    Raised when a step_id associated with a specific job cannot be found in a YAML file.
    """

    message_template = "Step_id '{step_id}' not found in job '{job_name}'"
