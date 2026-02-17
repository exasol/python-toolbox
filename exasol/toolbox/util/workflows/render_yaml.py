import io
from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path
from typing import Any

from jinja2 import (
    Environment,
    StrictUndefined,
    TemplateError,
)
from ruamel.yaml import (
    YAML,
    CommentedMap,
)
from ruamel.yaml.error import YAMLError

jinja_env = Environment(
    variable_start_string="((",
    variable_end_string="))",
    autoescape=True,
    # This requires that all Jinja variables must be defined in the provided
    # dictionary. If not, then a `jinja2.exceptions.UndefinedError` exception
    # will be raised.
    undefined=StrictUndefined,
)


class YamlOutputError(Exception):
    """
    Raised when the final workflow cannot be exported as a YAML file.
    This would likely indicate that one of the preceding transformation steps
    led to a format that is no longer able to be exported as a YAML file.
    """

    def __init__(self, file_path: Path):
        super().__init__(f"File '{file_path}' could not be output by ruamel-yaml.")


class YamlParsingError(Exception):
    """
    Raised when the rendered template is not a valid YAML file, as it cannot be
     parsed by ruamel-yaml.
    """

    def __init__(self, file_path: Path):
        super().__init__(
            f"File '{file_path}' could not be parsed by ruamel-yaml. "
            "Check for invalid YAML syntax in the workflow template."
        )


class TemplateRenderingError(Exception):
    """
    Raised when Jinja2 fails to modify the template. It may be that a Jinja
    variable was not defined, a brace was not closed, etc.
    """

    def __init__(self, file_path: Path):
        super().__init__(
            f"File '{file_path}' failed to render. Check Jinja2-related errors."
        )


@dataclass(frozen=True)
class YamlRenderer:
    """
    The :class:`YamlRenderer` provides a standardised interface for rendering YAML
    files within the PTB. To simplify configuration and reduce manual coordination,
    use Jinja variables as defined in :meth:`BaseConfig.github_template_dict` in your
    YAML files.
    """

    github_template_dict: dict[str, Any]
    file_path: Path

    @staticmethod
    def _get_standard_yaml() -> YAML:
        """
        Prepare standard YAML class.
        """
        yaml = YAML()
        yaml.width = 200
        yaml.preserve_quotes = True
        yaml.sort_base_mapping_type_on_output = False  # type: ignore
        yaml.indent(mapping=2, sequence=4, offset=2)
        return yaml

    def _render_with_jinja(self, input_str: str) -> str:
        """
        Render the template with Jinja.
        """
        jinja_template = jinja_env.from_string(input_str)
        return jinja_template.render(self.github_template_dict)

    def get_yaml_dict(self) -> CommentedMap:
        """
        Load a file as a CommentedMap (dictionary form of a YAML), after
        rendering it with Jinja.
        """
        with self.file_path.open("r", encoding="utf-8") as stream:
            raw_content = stream.read()

        try:
            workflow_string = self._render_with_jinja(raw_content)
            yaml = self._get_standard_yaml()
            return yaml.load(workflow_string)
        except TemplateError as exc:
            raise TemplateRenderingError(file_path=self.file_path) from exc
        except YAMLError as exc:
            raise YamlParsingError(file_path=self.file_path) from exc

    def get_as_string(self, yaml_dict: CommentedMap) -> str:
        """
        Output a YAML string.
        """
        yaml = self._get_standard_yaml()
        try:
            with io.StringIO() as stream:
                yaml.dump(yaml_dict, stream)
                workflow_string = stream.getvalue()
            return cleandoc(workflow_string)
        except YAMLError as exc:
            raise YamlOutputError(file_path=self.file_path) from exc
