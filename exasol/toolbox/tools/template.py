import difflib
import io
from collections.abc import Mapping
from contextlib import ExitStack
from inspect import cleandoc
from pathlib import Path
from typing import (
    Any,
)

import importlib_resources as resources
import typer
import yaml
from jinja2 import Environment
from rich.columns import Columns
from rich.console import Console
from rich.syntax import Syntax

from noxconfig import PROJECT_CONFIG

stdout = Console()
stderr = Console(stderr=True)

CLI = typer.Typer()

jinja_env = Environment(
    variable_start_string="((", variable_end_string="))", autoescape=True
)


def _templates(pkg: str) -> Mapping[str, Any]:
    def _normalize(name: str) -> str:
        name, _ = name.split(".")
        return name

    return {_normalize(w.name): w for w in resources.files(pkg).iterdir()}


def list_templates(columns: bool, pkg: str) -> None:
    """List all available templates."""

    class List:
        def __init__(self, items: Any):
            self.items = items

        def __rich__(self) -> str:
            return "\n".join(self.items)

    output = (
        List(_templates(pkg)) if not columns else Columns(_templates(pkg), expand=True)
    )
    stdout.print(output)


def show_templates(
    template: str,
    pkg: str,
    template_type: str,
    lexer: str,
) -> None:
    """Shows a specific template."""
    templates = _templates(pkg)
    if template not in templates:
        stdout.print(f"Unknown {template_type} <{template}>.", style="red")
        raise typer.Exit(code=1)

    template = templates[template]
    stdout.print(
        Syntax.from_path(path=template, encoding="utf-8", lexer=lexer)
    )  # type: ignore


def _render_template(
    src: str | Path,
    stack: ExitStack,
) -> str:
    input_file = stack.enter_context(open(src, encoding="utf-8"))

    # dynamically render the template with Jinja2
    template = jinja_env.from_string(input_file.read())
    rendered_string = template.render(PROJECT_CONFIG.github_template_dict)

    # validate that the rendered content is a valid YAML. This is not
    # written out as by default it does not give GitHub-safe output.
    yaml.safe_load(rendered_string)
    return cleandoc(rendered_string) + "\n"


def diff_template(template: str, dest: Path, pkg: str, template_type: str) -> None:
    """Diff a specific template against the installed one."""
    templates = _templates(pkg)
    if template not in templates:
        stdout.print(f"Unknown {template_type} <{template}>.", style="red")
        raise typer.Exit(code=1)

    # Use Any type to enable reuse of the variable/binding name
    for name, path in templates.items():
        if name == template:
            old: Any = dest / f"{template}{path.suffix}"
            new: Any = Path(_templates(pkg)[template])
            with ExitStack() as stack:
                old = stack.enter_context(
                    open(old, encoding="utf-8") if old.exists() else io.StringIO("")
                )
                if template_type == "issue":
                    new = stack.enter_context(open(new, encoding="utf-8"))
                    old = old.read().split("\n")
                    new = new.read().split("\n")
                elif template_type == "workflow":
                    new = _render_template(src=new, stack=stack)
                    old = old.read().split("\n")
                    new = new.split("\n")

            diff = difflib.unified_diff(old, new, fromfile="old", tofile="new")
            stdout.print(Syntax("\n".join(diff), "diff"))


def _install_template(
    template_type: str,
    src: str | Path,
    dest: str | Path,
    exists_ok: bool = False,
) -> None:
    src, dest = Path(src), Path(dest)

    if dest.exists() and not exists_ok:
        raise FileExistsError(f"{template_type} already exists")

    with ExitStack() as stack:
        if template_type == "issue":
            input_file = stack.enter_context(open(src, "rb"))
            output_file = stack.enter_context(open(dest, "wb"))
            output_file.write(input_file.read())
            return

        output_file = stack.enter_context(open(dest, "wb"))
        rendered_string = _render_template(src=src, stack=stack)
        output_file.write(rendered_string.encode("utf-8"))


def _select_templates(template: str, pkg: str, template_type: str) -> Mapping[str, Any]:
    templates = _templates(pkg)
    if template != "all" and template not in templates:
        raise Exception(f"{template_type} <{template}> is unknown")
    templates = (
        templates
        if template == "all"
        else {name: path for name, path in templates.items() if template == name}
    )
    return templates


def install_template(template: str, dest: Path, pkg: str, template_type: str) -> None:
    """
    Installs the requested template into the target directory.

    Attention: If there is an existing template with the same name it will be overwritten!
    """
    if not dest.exists():
        dest.mkdir(parents=True)

    try:
        templates = _select_templates(template, pkg, template_type)
    except Exception as ex:
        stderr.print(f"[red]{ex}[/red]")
        raise typer.Exit(-1)

    for name, path in templates.items():
        destination = dest / f"{name}{path.suffix}"
        _install_template(template_type, path, destination, exists_ok=True)
        stderr.print(f"Installed {name} in {destination}")


def update_template(
    template: str, dest: Path, confirm: bool, pkg: str, template_type: str
) -> None:
    """Similar to install but checks for existing templates and shows diff"""
    if not dest.exists():
        dest.mkdir(parents=True)

    try:
        templates = _select_templates(template, pkg, template_type)
    except Exception as ex:
        stderr.print(f"[red]{ex}[/red]")
        raise typer.Exit(-1)

    if confirm:
        install_template(template, dest, pkg, template_type)
        raise typer.Exit(0)

    for name, path in templates.items():
        destination = dest / f"{name}{path.suffix}"
        try:
            _install_template(template_type, path, destination, exists_ok=False)
            stderr.print(f"Updated {name} in {destination}")
        except FileExistsError:
            show_diff = typer.confirm(
                f"{template_type} <{name}> already exists, show diff?"
            )
            if show_diff:
                diff_template(name, dest, pkg, template_type)

            overwrite = typer.confirm(f"Overwrite existing {template_type}?")
            if overwrite:
                _install_template(template_type, path, destination, exists_ok=True)
                stderr.print(f"Updated {name} in {destination}")


if __name__ == "__main__":
    CLI()
