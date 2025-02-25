.. _styleguide:


:octicon:`paintbrush` Python Styleguide
=======================================

.. toctree::
    :maxdepth: 2
    :hidden:

    guides/style


Welcome
-------

Welcome to the Exasol_ python-styleguide.
This styleguide is not intend to be the holy bible on how to do each and every single detail in python,
it rather tries to reley on existing documents, guides and references (e.g. pep8_).
This guide rather is adds useful additions or exceptions where Exasol_ is diverging from the *"norm"*.

.. figure:: https://imgs.xkcd.com/comics/standards.png
    :alt: xkcd-1445
    :target: https://xkcd.com/1445/

    source: `xkcd.com <https://xkcd.com/>`_
    license: `CC BY-NC 2.5 <https://creativecommons.org/licenses/by-nc/2.5/>`_


.. note::

    This guide is a rolling release, so it always reflects the latest status quo. Still it may also happen that
    the information is missing or incomplete, in that case we want to encourage the reader to either create a PR
    or an Issue, to either track or fix those cases.

Before you start
----------------
As already mentioned this guide is a extension rather than a reference manual so before you jump right in,
we want you to take a moment and read through **The Zen of Python** if you haven't read it before.

.. code-block::

    >>> import this
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!

.. _Exasol: https://www.exasol.com/
.. _pep8: https://peps.python.org/pep-0008/
