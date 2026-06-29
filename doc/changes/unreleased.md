# Unreleased

## Summary

This minor release adds an opt-out for documentation-enabled workflows and jobs. Projects can
now declare that they do not serve documentation with the `has_documentation` switch in
`BaseConfig`, and the workflow generator/checker will stop expecting `pr-merge.yml` for
those projects. This should only be set to `False` for exceptional cases.

## Feature

* #901: Provided switch `has_documentation` in `BaseConfig` for projects without documentation
