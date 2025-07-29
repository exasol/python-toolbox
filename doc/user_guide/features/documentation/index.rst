.. _building_documentation:

Building documentation
======================

.. toctree::
    :maxdepth: 2

    multiversion
    troubleshooting

In the PTB, we use sphinx to build and validate the contents of a project's
documentation. All documentation is provided in the ``doc`` directory, primarily as
`rst` files. The ``doc/conf.py`` acts as the configuration file for building the
documentation.

Many of the nox session checks are executed in the ``checks.yml`` so that alterations
in the documentation can be directly attributed (and, if needed, fixed) in the relevant
PR. The final building & serving of the documentation happens in the ``gh-pages.yml``.

+--------------------------+------------------+----------------------------------------+
| Nox session              | CI Usage         | Action                                 |
+==========================+==================+========================================+
| ``docs:build``           | ``checks.yml``   | Builds the documentation               |
+--------------------------+------------------+----------------------------------------+
| ``docs:clean``           | No               | Removes the documentation build folder |
+--------------------------+------------------+----------------------------------------+
| ``docs:multiversion``    | ``gh-pages.yml`` | Builds the multiversion documentation  |
+--------------------------+------------------+----------------------------------------+
| ``docs:open``            | No               | Opens the built documentation          |
+--------------------------+------------------+----------------------------------------+
| ``links:check``          | ``checks.yml``   | Checks if all links in the             |
|                          |                  | documentation are accessible           |
+--------------------------+------------------+----------------------------------------+
| ``links:list``           | No               | Lists all links in the documentation   |
+--------------------------+------------------+----------------------------------------+
