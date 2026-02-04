from dataclasses import dataclass
from itertools import count
from typing import Any

from jinja2 import Environment

jinja_env = Environment(
    variable_start_string="((", variable_end_string="))", autoescape=True
)

import io
from inspect import cleandoc

from ruamel.yaml import YAML


@dataclass(frozen=True)
class TemplateToWorkflow:
    template_str: str
    github_template_dict: dict[str, Any]
    _comment_id: count = count(0)

    def _render_with_jinja(self, input_str: str) -> str:
        """
        Render the template with Jinja.
        """
        jinja_template = jinja_env.from_string(input_str)
        return jinja_template.render(self.github_template_dict)

    def convert(self) -> str:
        """
        Convert a workflow template to a rendered workflow that works for GitHub.
        """
        yaml = YAML()
        yaml.width = 200
        yaml.preserve_quotes = True
        yaml.sort_base_mapping_type_on_output = False  # Ensures keys stay in order
        yaml.indent(mapping=2, sequence=4, offset=2)

        workflow_string = self._render_with_jinja(self.template_str)
        workflow_dict = yaml.load(workflow_string)

        stream = io.StringIO()
        yaml.dump(workflow_dict, stream)
        workflow_string = stream.getvalue()
        return cleandoc(workflow_string)
