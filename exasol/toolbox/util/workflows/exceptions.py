from pathlib import Path


class YamlError(Exception):
    """Base exception for YAML errors."""

    message_template = "An error occurred with file: {file_path}"

    def __init__(self, file_path: Path):
        self.file_path = file_path
        # Format the template defined in the subclass
        message = self.message_template.format(file_path=file_path)
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


class YamlKeyError(Exception):
    """
    Base exception for when a specified value cannot be found in a YAML.
    """

    message_template = "An error occurred with job: '{job_name}'"

    def __init__(self, job_name: str):
        self.job_name = job_name
        # Format the template defined in the subclass
        message = self.message_template.format(job_name=job_name)
        super().__init__(message)


class YamlJobValueError(Exception):
    """
    Raised when a job cannot be found in a YAML file.
    """

    message_template = "Job '{job_name}' could not be found"

    def __init__(self, job_name: str):
        self.job_name = job_name
        # Format the template defined in the subclass
        message = self.message_template.format(job_name=job_name)
        super().__init__(message)


class YamlStepIdValueError(YamlKeyError):
    """
    Raised when a step_id associated with a specific job cannot be found in a YAML file.
    """

    message_template = "Step_id '{step_id}' not found in job '{job_name}'"

    def __init__(self, step_id: str, job_name: str):
        self.step_id = step_id
        self.job_name = job_name

        message = self.message_template.format(step_id=step_id, job_name=job_name)
        super(YamlKeyError, self).__init__(message)
