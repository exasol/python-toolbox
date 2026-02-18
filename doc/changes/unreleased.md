# Unreleased

## Summary

## Feature

* #691: Started customization of PTB workflows by defining the YML schema
* #712: Added basic logging to workflow processing
* #714: Added logic to modify a workflow using the .workflow-patcher.yml

## Refactoring

* #664: Removed deprecation warning for projects to switch over to BaseConfig
* #637: Added id to workflow templates  & synchronized on naming conventions
* #702: Fixed StepCustomization.content to list[StepContent] and security concern for `update_cookiecutter_default`
* #710: Refactored and added custom exceptions to YamlRender-based classes
