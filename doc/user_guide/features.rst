Features
========

Uniform Project Layout
----------------------

PTB expects a default project layout following "convention over configuration" when possible and reasonable.
See the cookie-cutter project template for details, which is part of the python-toolbox workspace and can be found in directory `project-template`.
You can also generate a project from the template to explore the default structure.
For more details on this, please check out section :ref:`Getting Started` section.

Nox
---

The most central tool when interacting with the toolbox is :code:`nox`, which is the task runner used across all of Exasol's Python-based projects.
The toolbox itself provides various standard tasks and a plugin mechanism to extend these tasks if needed. For more information regarding nox, please visit the `nox homepage <http://nox.thea.codes/en/stable/>`_.

Central files in regards to nox and the toolbox are:

- noxfile.py: Standard nox configuration/setup file
- noxconfig.py: Exasol-specific file containing additional information needed by the standard tasks of the toolbox

Important Nox Commands
^^^^^^^^^^^^^^^^^^^^^^

* :code:`nox -l` shows a list of all available nox tasks
* :code:`nox -s <tasks>` run the specified task(s)
    * :code:`nox -s test:typing` runs the type checker on the project
    * :code:`nox -s docs:clean docs:build docs:open`
        #. first task removes the documentation folder
        #. second one builds the documentation
        #. last one opens the documentation in the web browser
* :code:`nox` without :code:`-s` runs the default task which is
    * :code:`nox -s project:fix` this command runs automated fixes on the code
