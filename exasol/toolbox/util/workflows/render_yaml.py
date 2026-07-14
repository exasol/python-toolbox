import io
from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateError,
)
from pydantic import (
    BaseModel,
    ConfigDict,
)
from ruamel.yaml import (
    YAML,
    CommentedMap,
)
from ruamel.yaml.error import YAMLError

from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import (
    TemplateRenderingError,
    YamlOutputError,
    YamlParsingError,
)
from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS


class GithubTemplateContext(BaseModel):
    """Immutable template values exposed to Jinja workflow rendering."""

    model_config = ConfigDict(frozen=True)

    custom_workflows: dict[str, object]
    dependency_manager_version: str
    has_documentation: bool
    minimum_python_version: str
    os_version: str
    python_versions: tuple[str, ...]
    sonar_token_name: str
    workflow_header: str


def build_jinja_env(template_path: Path) -> Environment:
    """
    Create a Jinja environment for a workflow template file.
    """
    workflow_template_directory = WORKFLOW_TEMPLATE_OPTIONS["ci"].parent
    return Environment(
        loader=FileSystemLoader([template_path.parent, workflow_template_directory]),
        variable_start_string="((",
        variable_end_string="))",
        autoescape=True,
        # This requires that all Jinja variables must be defined in the provided
        # dictionary. If not, then a `jinja2.exceptions.UndefinedError` exception
        # will be raised.
        undefined=StrictUndefined,
        block_start_string="(%",
        block_end_string="%)",
        trim_blocks=True,  # Removes the newline after a block
        lstrip_blocks=True,  # Removes tabs/spaces before a block
    )


def get_standard_yaml() -> YAML:
    """
    Prepare standard YAML class.
    """
    yaml = YAML()
    yaml.width = 200
    yaml.preserve_quotes = True
    yaml.sort_base_mapping_type_on_output = False  # type: ignore
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def parse_yaml_text(origin_path: Path, workflow_string: str) -> CommentedMap:
    """
    Parse YAML from text while keeping the origin path for diagnostics.
    """
    try:
        yaml = get_standard_yaml()
        logger.debug("Parse %s with ruamel-yaml", origin_path)
        return yaml.load(workflow_string)
    except YAMLError as ex:
        raise YamlParsingError(file_path=origin_path) from ex


@dataclass(frozen=True)
class YamlRenderer:
    """
    The :class:`YamlRenderer` provides a standardised interface for rendering YAML
    files within the PTB. To simplify configuration and reduce manual coordination,
    use Jinja variables as defined in :meth:`BaseConfig.github_template_dict` in your
    YAML files.
    """

    github_template_dict: GithubTemplateContext
    file_path: Path

    def _render_with_jinja(self, input_str: str) -> str:
        """
        Render the template with Jinja.
        """
        logger.debug(
            "Render template with Jinja",
            jinja_dict_source="PROJECT_CONFIG.github_template_dict",
        )
        jinja_template = build_jinja_env(self.file_path).from_string(input_str)
        if isinstance(self.github_template_dict, dict):
            render_context = self.github_template_dict
        else:
            render_context = self.github_template_dict.model_dump()
        return jinja_template.render(**render_context)

    def get_yaml_dict(self) -> CommentedMap:
        """
        Load a file as a CommentedMap (dictionary form of a YAML), after
        rendering it with Jinja.
        """
        raw_content = self.file_path.read_text()
        try:
            workflow_string = self._render_with_jinja(raw_content)
        except TemplateError as ex:
            raise TemplateRenderingError(file_path=self.file_path) from ex
        return parse_yaml_text(
            origin_path=self.file_path, workflow_string=workflow_string
        )

    def get_as_string(self, yaml_dict: CommentedMap) -> str:
        """
        Output a YAML string.
        """
        yaml = get_standard_yaml()
        try:
            logger.debug("Output workflow as string")
            with io.StringIO() as stream:
                yaml.dump(yaml_dict, stream)
                workflow_string = stream.getvalue()
            return cleandoc(workflow_string)
        except YAMLError as ex:
            raise YamlOutputError(file_path=self.file_path) from ex
