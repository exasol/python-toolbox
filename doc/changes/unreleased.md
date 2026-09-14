# Unreleased

## Summary

This major release removes the deprecated matrix sessions ``matrix:all``,
``matrix:exasol``, and ``matrix:python``. Projects should use ``matrix.yml`` together
with the ``matrix:generate`` Nox session instead.

## Refactoring

* #859: Removed the deprecated ``matrix:all``, ``matrix:exasol``, and ``matrix:python``
  Nox sessions.
