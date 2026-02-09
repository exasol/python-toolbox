from dataclasses import dataclass
from typing import Any

from jinja2 import Environment

from exasol.toolbox.util.workflows.format_yaml import get_standard_yaml

jinja_env = Environment(
    variable_start_string="((", variable_end_string="))", autoescape=True
)

import io
from inspect import cleandoc


@dataclass(frozen=True)
class TemplateRenderer:
    template_str: str
    github_template_dict: dict[str, Any]

    def _render_with_jinja(self, input_str: str) -> str:
        """
        Render the template with Jinja.
        """
        jinja_template = jinja_env.from_string(input_str)
        return jinja_template.render(self.github_template_dict)

    def render_to_workflow(self) -> str:
        """
        Render the template to the contents of a valid GitHub workflow.
        """
        workflow_string = self._render_with_jinja(self.template_str)

        yaml = get_standard_yaml()
        workflow_dict = yaml.load(workflow_string)

        stream = io.StringIO()
        yaml.dump(workflow_dict, stream)
        workflow_string = stream.getvalue()
        return cleandoc(workflow_string)
