# 11.0.0 - 2026-09-15

## Summary

This major release removes the deprecated matrix sessions ``matrix:all``,
``matrix:exasol``, and ``matrix:python``. Projects should use ``matrix.yml`` together
with the ``matrix:generate`` Nox session instead.

## Refactoring

* #859: Removed the deprecated ``matrix:all``, ``matrix:exasol``, and ``matrix:python``
  Nox sessions.

## Dependency Updates

### `main`

* Updated dependency `coverage:7.16.0` to `7.16.1`
* Updated dependency `sphinx-toolbox:4.3.0` to `4.3.1`
* Updated dependency `sphinxcontrib-mermaid:2.1.0` to `2.1.1`
* Updated dependency `zizmor:1.30.0` to `1.30.1`

### `dev`

* Updated dependency `types-pyyaml:6.0.12.20260815` to `6.0.12.20260906`
