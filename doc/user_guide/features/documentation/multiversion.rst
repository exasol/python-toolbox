sphinx-multiversion
===================

The ``sphinx-multiversion`` extension is a modified copy of
`sphinx-contrib/multiversion <https://github.com/sphinx-contrib/multiversion>`__.
This copy was taken from version :code:`0.24.0`.

It has been modified to work with Exasol's integration projects, which often require a
specific project structure and layout. Additionally, it is designed to be used with an
HTML theme that supports displaying and selecting multiple versions if the `versions`
variable is set in the HTML context of sphinx. As of this writing, the theme used in
conjunction with this modified version of ``sphinx-multiversion`` is
`SHIBUYA <https://github.com/lepture/shibuya>`__.

.. attention::

    **Attribution**

    A big thanks to the original author and project
    `Jan Holthuis <https://github.com/Holzhaus>`_, as well as
    `Samuel Dowling <https://github.com/samuel-emrys>`_, as we took various patches for
    the plugin from his fork.

    Note: Both projects are published under the `BSD-2 license <https://opensource.org/license/bsd-2-clause>`_.

    * https://github.com/sphinx-contrib/multiversion
    * https://github.com/samuel-emrys/sphinx-multiversion

.. note::

    In the long term, it would be advantageous to remove unnecessary features and code
    that are not required for Exasol's projects. Adding further tests would also be
    beneficial. However, the primary goal was to create a low-effort, stable
    multi-version support solution for our projects.
