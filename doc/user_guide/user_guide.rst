.. _user_guide:

:octicon:`person` User Guide
============================

.. toctree::
    :maxdepth: 2
    :hidden:

    dependencies
    getting_started
    configuration
    features/index
    troubleshooting/index
    customization
    migrating

Exasol's Python Toolbox (PTB) helps you creating and maintaining your Python projects.

PTB simplifies keeping all of our projects up-to-date, secure, without bugs, using uniform code style and formatting, correctly typed, decent quality wrt. static code analysis, nicely documented, and equipped with a unified CI/CD pipeline for building, testing, and publishing their artifacts.

The PTB gains its name from employing a series of well-established tools to satisfy these goals:

* `Poetry`_ for packaging and managing dependencies
* `Nox`_ for using the tools via a common CLI
* `Black`_ and `Ruff`_ for source code formatting
* `Pylint`_ / ruff for linting
* `Cookiecutter`_ for setting up new projects from a uniform template
* `Mypy`_ for static type checking
* `Coverage`_ for measuring code coverage by tests
* `Bandit`_ for detecting security vulnerabilities
* `Sphinx`_ for generating the documentation
* `Sonar`_ for reporting code quality based on the findings by other tools

In rare cases you may need to disable a particular finding reported by one of
these tools, see :ref:`ptb_troubleshooting`.

.. _Poetry: https://python-poetry.org
.. _Nox: https://nox.thea.codes/en/stable/
.. _Black: https://black.readthedocs.io/en/stable/
.. _Ruff: https://docs.astral.sh/ruff
.. _Pylint: https://pylint.readthedocs.io/en/stable/
.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/stable/
.. _Mypy: https://mypy.readthedocs.io/en/stable/
.. _Coverage: https://coverage.readthedocs.io/en/7.13.4/
.. _Bandit: https://bandit.readthedocs.io/en/latest/
.. _Sphinx: https://www.sphinx-doc.org/en/master
.. _Sonar: https://docs.sonarsource.com/sonarqube-server
