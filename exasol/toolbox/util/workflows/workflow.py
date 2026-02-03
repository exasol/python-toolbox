from inspect import cleandoc
from pathlib import Path
from typing import Any

from jinja2 import Environment
from pydantic import (
    BaseModel,
    ConfigDict,
)
from yaml import (
    dump,
    safe_load,
)

from exasol.toolbox.util.workflows.format_yaml import GitHubDumper

jinja_env = Environment(
    variable_start_string="((", variable_end_string="))", autoescape=True
)


def _render_template(template: str, github_template_dict: dict[str, Any]) -> str:
    """
    Render the template with Jinja2 & dump as a str
    """
    # Dynamically render the template with Jinja2
    jinja_template = jinja_env.from_string(template)
    rendered_string = jinja_template.render(github_template_dict)

    # Also checks that the rendered template is a valid YAML.
    data = safe_load(rendered_string)

    return cleandoc(
        dump(
            data,
            Dumper=GitHubDumper,
            sort_keys=False,  # if True, then re-orders the jobs alphabetically
        )
    )


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(cls, file_path: Path, github_template_dict: dict[str, Any]):
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        try:
            raw_content = file_path.read_text()
            rendered_content = _render_template(
                template=raw_content, github_template_dict=github_template_dict
            )
            return cls(content=rendered_content)
        except Exception as e:
            raise ValueError(f"Error rendering file: {str(e)}")
