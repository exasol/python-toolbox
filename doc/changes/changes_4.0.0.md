# 4.0.0 - 2025-12-09

## Summary

This major release removes `project:fix` and `project:format`
and replaces them with `format:fix` and `format:check`.

The `BaseConfig` has been extended to handle the commonly provided paths:
* `root` is now `root_path`
* `source` is now covered by `project_name` and `source_code_path`, which uses `root_path` and `project_name`
* `doc` is now `documentation_path`
* `version_file` is now `version_filepath`

If your project was previously defining these values, your **before** would look like:

```python
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from exasol.toolbox.config import BaseConfig


class Config(BaseConfig):
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    source: Path = Path("exasol/{{cookiecutter.package_name}}")
    version_file: Path = (
            Path(__file__).parent
            / "exasol"
            / "{{cookiecutter.package_name}}"
            / "version.py"
    )
    plugins: Iterable[object] = ()

PROJECT_CONFIG = Config()
```

With this major release, you **should modify** your project's `noxconfig.py` to look like:
```python
from __future__ import annotations

from pathlib import Path

from exasol.toolbox.config import BaseConfig

"""
A class `Config` only needs to be defined if:
- you have custom attributes to pass to your project-defined nox sessions
- you need to override a convention in the PTB.

These values do NOT need to be defined if your project follows the convention
expected from the PTB:
- documentation_path
- source_code_path
- version_filepath

If your values differ, you can override these properties with the needed values when
you define `class Config(BaseConfig)`. We highly recommend that you create an issue
to remove this override in the future by aligning your project's structure with
that expected by the PTB.

If you have additional Paths that used one of these values (i.e. `root_path`), then
you can define your own property in `class Config(BaseConfig)`, which accesses the
class values
"""
class Config(BaseConfig):
    custom_field: str = "custom_field"

# For most projects, the PROJECT_CONFIG would look like:
PROJECT_CONFIG = BaseConfig(
    project_name="{{cookiecutter.package_name}}",
    root_path=Path(__file__).parent,
)
```

## Refactoring

* #606: Renamed nox session `project:fix` more aptly to `format:fix` and `project:format` to `format:check`
* #604: Updated `BaseConfig.exasol_versions` to `("7.1.30", "8.29.13", "2025.1.8")`

## Feature

* #614: Replaced `path_filters` with `BaseConfig.add_to_excluded_python_paths` and `BaseConfig.excluded_python_paths`
* #626: Replaced `plugins` with `BaseConfig.plugins_for_nox_sessions`
* #621: Moved path specifications into `BaseConfig`
  * `root` is now `root_path`, which must be specified by the project
  * `source` is now covered by `project_name`, which must be specified by the project,
     and `source_code_path`, which uses `root_path` and `project_name`
  * `doc` is now `documentation_path` and no longer needs to be specified
  * `version_file` is now `version_filepath` and no longer needs to be specified

## Dependency Updates

### `main`
* Updated dependency `bandit:1.9.1` to `1.9.2`
* Updated dependency `mypy:1.18.2` to `1.19.0`
* Updated dependency `pre-commit:4.4.0` to `4.5.0`
* Updated dependency `pydantic:2.12.4` to `2.12.5`
* Updated dependency `pylint:4.0.3` to `4.0.4`
* Updated dependency `ruff:0.14.5` to `0.14.8`
