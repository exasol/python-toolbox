# 1.10.0 - 2025-10-10
New `BasConfig` class and improved Setup Python Github Action.

## BaseConfig class for PTB attributes

The BaseConfig class was introduced in this version. This class is used to consolidate
the attributes needed for the PTB's functionalities into an inherited object which can
be expanded upon as needed. At this point, the BaseConfig class includes
``python_versions``, ``exasol_versions``, and ``create_major_version_tags``. Users of
the PTB should update their ``noxconfig.py`` to start using this feature.

```python
# noxconfig.py
from exasol.toolbox.config import BaseConfig


# existing Config should inherit from BaseConfig
class Config(BaseConfig):
    # if present, remove any attributes already in the BaseConfig from the added attributes
    ...


# if no overlapping attributes with `BaseConfig` were present in `Config`, then this is unmodified.
PROJECT_CONFIG = Config()
# if no overlapping attributes with `BaseConfig` were present in `Config`, then this should be modified.
PROJECT_CONFIG = Config(python_versions=(...), exasol_versions=(...), create_major_version_tags=True)
```

## Feature

* #465: Created BaseConfig class to better synchronize attributes needed for the PTB's
  growing functionalities

## Internal:

* Call poetry install always in setup python actions

## Dependency Updates

### `main`
* Updated dependency `coverage:7.10.3` to `7.10.6`
* Updated dependency `import-linter:2.3` to `2.4`
* Updated dependency `shibuya:2025.7.24` to `2025.8.16`
* Added dependency `sphinx-toolbox:4.0.0`
* Updated dependency `typer:0.16.0` to `0.17.3`
