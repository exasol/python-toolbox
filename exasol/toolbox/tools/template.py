import difflib
import io
from contextlib import ExitStack
from pathlib import Path
from typing import (
    Any,
    Mapping,
    Union,
)

import importlib_resources as resources
import typer
from rich.columns import Columns
from rich.console import Console
from rich.syntax import Syntax

stdout = Console()
stderr = Console(stderr=True)

CLI = typer.Typer()


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
    stdout.print(Syntax.from_path(path=template, encoding="utf-8", lexer=lexer))  # type: ignore


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
                new = stack.enter_context(open(new, encoding="utf-8"))
                old = old.read().split("\n")
                new = new.read().split("\n")

            diff = difflib.unified_diff(old, new, fromfile="old", tofile="new")
            stdout.print(Syntax("\n".join(diff), "diff"))


def _install_template(
    template_type: str,
    src: Union[str, Path],
    dest: Union[str, Path],
    exists_ok: bool = False,
) -> None:
    src, dest = Path(src), Path(dest)

    if dest.exists() and not exists_ok:
        raise FileExistsError(f"{template_type} already exists")

    with ExitStack() as stack:
        input_file = stack.enter_context(open(src, "rb"))
        output_file = stack.enter_context(open(dest, "wb"))
        output_file.write(input_file.read())


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
        dest.mkdir()

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
        dest.mkdir()

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
