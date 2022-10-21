"""
Git based multi version support for sphinx.

This module/plugin provides support for creating a multi version output for the documented project.
Version's are defined using git tags and branches, the only supported output format is html.

NOTICE:
The original version of this package was published under the BSD license and can be found `here <https://github.com/Holzhaus/sphinx-multiversion>`_.
We also took some patches from `this <https://github.com/samuel-emrys/sphinx-multiversion>`_ which was also published under the BSD license.

So huge thanks to the original author `Jan Holthuis <https://github.com/Holzhaus>`_ and all contributors.

TODO's:
* add standard default templates
* add support for index page
* add sorting support
* add gh pages support
* add command to deploy to gh-pages
* add support for loading packed version template?
"""

from exasol.toolbox.sphinx.multiversion.main import main

__version__ = "0.1.0"

__all__ = [
    "setup",
    "main",
]
