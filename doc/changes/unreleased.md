# Unreleased

## Summary

From exasol-toolbox version ``1.0.0`` the default behavior for ``.github/actions/python-environment/action.yml``
has changed. In previous versions, the default value for ``poetry-version`` was ``1.2.2``,
and it is now ``2.1.2``. 

* Depending on its poetry version, a repository relying on the default behavior of said 
action may run into breaking changes. This can easily be resolved with explicitly setting the
`poetry-version` when calling the GitHub action. It is, however, recommended whenever
possible to update the poetry version of affected repository to ``2.x``.

## ✨ Features

* [#73](https://github.com/exasol/python-toolbox/issues/73): Added nox target for auditing work spaces in regard to known vulnerabilities
* [#65](https://github.com/exasol/python-toolbox/issues/65): Added a Nox task for checking if the changelog got updated.
* [#369](https://github.com/exasol/python-toolbox/issues/369): Removed option `-v` for `isort`
* [#372](https://github.com/exasol/python-toolbox/issues/372): Added conversion from pip-audit JSON to expected GitHub Issue format

## ⚒️ Refactorings
* [#388](https://github.com/exasol/python-toolbox/issues/388): Switched GitHub workflows to use pinned OS version
* [#376](https://github.com/exasol/python-toolbox/issues/376): Updated to poetry ``2.1.2``