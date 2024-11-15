"""
Git based multi version support for sphinx.

This module/plugin provides support for creating a multi version output for the documented project.
Version's are defined using git tags and branches, the only supported output format is html.

NOTICE:
The original version of this package was published under the BSD license and can be found `here <https://github.com/Holzhaus/sphinx-multiversion>`_.
We also took some patches from `this <https://github.com/samuel-emrys/sphinx-multiversion>`_ which was also published under the BSD license.

So huge thanks to the original author `Jan Holthuis <https://github.com/Holzhaus>`_ and all contributors.


NOTE:
The original version and its defaults were minimally adjusted to work in Exasol's projects with the defaults and without adding an extra template. The [Shibuya](https://github.com/lepture/shibuya) theme is expected to be used for HTML, which already evaluates the versions field in the HTML context and generates an appropriate selector for the versions.
"""

from exasol.toolbox.sphinx.multiversion.main import main
from exasol.toolbox.sphinx.multiversion.sphinx import setup
from exasol.toolbox.version import VERSION

__version__ = VERSION

__all__ = [
    "setup",
    "main",
]
