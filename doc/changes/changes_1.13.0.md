# 1.13.0 - 2025-10-31

## Summary

This releases fixes Nox session `release:prepare` for multi-project repositories and
fixes the `python-environment` GitHub action to also use the `working-directory`
and `pyproject.toml` setting the cache variables.

## Bugfixes

* #580: Fixed Nox session `release:prepare` for multi-project repositories
* #586: Fixed `python-environment` GitHub action to use `working-directory` for setup of cache variables
* #559: Added SHA of `pyproject.toml` to determine cache key in `python-environment` GitHub action

## Features

* #485: Improved nox task `release:trigger`
