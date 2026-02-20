# Unreleased

## Summary

## Feature

* #691: Started customization of PTB workflows by defining the YML schema
* #712: Added basic logging to workflow processing
* #714: Added logic to modify a workflow using the .workflow-patcher.yml
* #717: Restricted workflow names in .workflow-patcher.yml to template workflow names
* #719: Added nox session `workflow:generate` to generate/update workflows using the `.workflow-patcher.yml` (if desired)

## Documentation

* #705: Described how the versions of poetry and python are retrieved
* #706: Added description how to ignore findings to the User Guide

## Refactoring

* #664: Removed deprecation warning for projects to switch over to BaseConfig
* #637: Added id to workflow templates  & synchronized on naming conventions
* #702: Fixed StepCustomization.content to list[StepContent] and security concern for `update_cookiecutter_default`
* #710: Refactored and added custom exceptions to YamlRender-based classes
