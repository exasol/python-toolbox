Design Document
===============

* Convention over configuration
* Documentation related stuff should be handled by sphinx + sphinx extensions ...
* Optional features and their depencies which are not needed by all projects should be enabled/disabled via feature flags
* Extension via overwriting pre defined nox targets
* noxconfig.py module which shall contain configuration
    - Import in tasks should check if noxconfig is in path, if not issue a concrete error and tell what to do (create noxconfig.py which is in the python path)
* Migration to Setting Type provided by lib
    - Settings class can provide properties and show deprecation warnings if option changes ..
