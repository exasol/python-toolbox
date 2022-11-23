Getting Started
===============

How to use the python toolbox
------------------------------

#. Add the toolbox as dependency

    .. code-block:: shell

        poetry add --dev exasol-toolbox

#. Add a noxconfig.py file containing a settings object which provides the following attributes

    .. literalinclude:: ../../noxconfig.py
       :language: python3


#. Make sure you configured the required tool(s)

    * coverage (files custom)
    * pylint (files custom)
    * black (provided)
    * isort (provided)
    * mypy (files & suppression custom)



    Example configuration

    .. code-block:: toml

        [tool.coverage.run]
        source = [
            "exasol",
        ]

        [tool.coverage.report]
        fail_under = 20


        [tool.black]
        line-length = 88
        verbose = false
        include = "\\.pyi?$"


        [tool.isort]
        profile = "black"
        force_grid_wrap = 2


        [tool.pylint.master]
        fail-under = 7.4

        [tool.pylint.format]
        max-line-length = 88
        max-module-lines = 800


        [[tool.mypy.overrides]]
        module = [
            "exasol.toolbox.sphinx.multiversion.*",
            "test.unit.*",
            "test.integration.*",
        ]
        ignore_errors = true


#. Import the toolbox tasks in your noxfile

    .. literalinclude:: ../../noxfile.py
       :language: python3


Run/Use Tasks locally
---------------------


Generate CI & CI/CD workflows
-----------------------------

* ci.yml
* ci-cd.yml (Github secret for pypi required!)
* pr-merge.yml




* add .html-documenation to .gitignore
