# Unreleased

## Summary

* Update `cd.yml` workflow so that `cd-extension.yml` workflow depends on `build-and-publish`. This ensures that the custom release workflow only runs when the PyPi release was successful.
