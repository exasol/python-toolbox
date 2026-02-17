import io
from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path
from typing import Any

from jinja2 import Environment
from ruamel.yaml import (
    YAML,
    CommentedMap,
)

jinja_env = Environment(
    variable_start_string="((", variable_end_string="))", autoescape=True
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

        workflow_string = self._render_with_jinja(raw_content)

        yaml = self._get_standard_yaml()
        return yaml.load(workflow_string)

    def get_as_string(self, yaml_dict: CommentedMap) -> str:
        """
        Output a YAML string.
        """
        yaml = self._get_standard_yaml()
        with io.StringIO() as stream:
            yaml.dump(yaml_dict, stream)
            workflow_string = stream.getvalue()
        return cleandoc(workflow_string)
