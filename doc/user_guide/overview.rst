Overview
========

Project Layout 
--------------

Overall, the toolbox generally expects a certain project layout because it tries to follow the credo "convention over configuration" when possible and reasonable. This expected structure can be better understood by looking at the cookie-cutter project template, which is part of the python-toolbox workspace and can be found in `project-template`. One can also generate a project from the template to explore the default structure. For more details on this, please check out the getting started section.

Nox
---

The most central tool when interacting with the toolbox is :code:`nox`, which is the task runner used across all of Exasol's Python-based projects.
The toolbox itself provides various standard tasks and a plugin mechanism to extend these tasks if needed. For more information regarding nox, please visit the `nox homepage <http://nox.thea.codes/en/stable/>`_.

Central files in regards to nox and the toolbox are:

- noxfile.py: Standard nox configuration/setup file
- noxconfig.py: Exasol-specific file containing additional information needed by the standard tasks of the toolbox
