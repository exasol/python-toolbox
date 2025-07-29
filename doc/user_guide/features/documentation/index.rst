.. _deploying_documentation:

Deploying documentation
=======================

.. toctree::
    :maxdepth: 2

    multiversion
    troubleshooting

The PTB uses ref:`sphinx <https://www.sphinx-doc.org/>`__ to build and validate the contents
of your project's documentation. PTB expects the project's documentation in directory ``doc``,
primarily as ``rst`` files. The ``doc/conf.py`` acts as the configuration file for building the
documentation.

GitHub workflow ``checks.yml`` also runs the checks for the documention.
This enables updating and fixing the documentation together with other changes in the same pull request.
The final building & serving of the documentation happens in GitHub workflow ``gh-pages.yml``.

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

.. _documentation_configuration:

Configuration
+++++++++++++

``doc/conf.py``
^^^^^^^^^^^^^^^
The PTB's cookiecutter project template already provides a file ``doc/conf.py`` with
default content. If your project needs adjustment, please refer to:

* the `general sphinx documentation <https://www.sphinx-doc.org/en/master/>`__.
* specifically to the `Linkcheck Builder <https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder>`__
  for ``links:check`` and ``links:list``.

``gh-pages.yml``
^^^^^^^^^^^^^^^^
GitHub workflow ``gh-pages.yml`` uses actions ``upload-pages-artifact`` and ``deploy-pages``.
In order to properly deploy your generated documentation, you will need to manually
reconfigure the GitHub Pages settings for the repo:

#. Go to the affected repo's GitHub page
#. Select 'Settings'
#. Scroll down & select 'Pages'
#. Within the 'Build and deployment' section, change 'Source' to 'GitHub Actions'.

You also need to configure settings for the `github-pages` environment:

#. Go to the affected repo's GitHub page
#. Select 'Settings'
#. Scroll down & select 'Environment'
#. Click on 'github-pages'
#. In the 'Deployment branches and tags', click 'Add deployment branch or tag rule'
#. Select 'Ref type' to be 'Tag' and set the 'Name pattern' to `[0-9]*.[0-9]*.[0-9]*` (or whatever matches that repo's tags)
