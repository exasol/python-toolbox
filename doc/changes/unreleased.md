# Unreleased

## Summary

With #420, any GitHub repos using the PTB for **documentation** will also need to
reconfigure the GitHub Pages settings for each repo:
1. Go to the affected repo's GitHub page
2. Select 'Settings'
3. Scroll down & select 'Pages'
4. Within the 'Build and deployment' section, change 'Source' to 'GitHub Actions'.

This should also create a 'github-pages' environment, if it does not yet exist.
For most repos using the PTB, the updating of the github pages only happens when a
PR is merged to main, so please check post-merge that it worked as expected.

With #422, we have hardened the security in our GitHub workflows by explicitly
setting permissions to the default GitHub token. In a few repos who greatly differ
from the default PTB setup, this might lead to small issues which require the allowed
permissions to be increased for specific jobs.

## ⚒️ Refactorings

* [#412](https://github.com/exasol/python-toolbox/issues/392):  Refactored pre commit hook package version.py into nox task

## Security

* [#420](https://github.com/exasol/python-toolbox/issues/420): Replaced 3rd party action with GitHub actions for gh-pages
* [#422](https://github.com/exasol/python-toolbox/issues/422): Set permissions within the GitHub workflows to restrict usage of the default GitHub token

## ✨ Features

* [#161](https://github.com/exasol/python-toolbox/issues/161): Added support for installing extras & not using a cache to the python-environment action
* [#408](https://github.com/exasol/python-toolbox/issues/408): Added support for GitHub runners who do not per default have pipx to use the python-environment action
* #433: Removed directory .html-documentation/.doctrees after creating documentation
* #436: Updated template for new projects to poetry 2.x

## Bugfixes

* #428: Fixed detecting report coverage failures
