# 1.9.0 - 2025-08-28
This release fixes stability problems with the Github action `python-environment`. Optionally, the nox task `release:trigger` now creates an additional tag with pattern `v<MajorVersion>`.

## Refactorings

 - #530: Nox task `release:trigger` also creates `v*` tag
 - #553: Use Local copy of poetry installer in Github actions `python-environment`
