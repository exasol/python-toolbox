General
-------

Named Parameters
++++++++++++++++
Use named parameters for inline primitive types (when it makes the call site easier to understand).

.. tab:: ✅ Good

    .. literalinclude:: ../../../_static/idioms/named_parameters.py
        :language: python3
        :start-after: # Good
        :end-before: # Bad

.. tab:: ❌ Bad

    .. literalinclude:: ../../../_static/idioms/named_parameters.py
        :language: python3
        :start-after: # Bad

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/named_parameters.py
        :language: python3

.. note::

    Consider using `keyword only arguments <https://peps.python.org/pep-3102/>`_ when defining API's.

**💡 learnt from:**

* Source: `Raymond Hettinger`_
* Reference: `Transform Python Slides`_

Unpacking
+++++++++

.. tab:: ✅ Good

    .. literalinclude:: ../../../_static/idioms/unpacking.py
        :language: python3
        :start-after: # Good
        :end-before: # Bad

.. tab:: ❌ Bad

    .. literalinclude:: ../../../_static/idioms/unpacking.py
        :language: python3
        :start-after: # Bad

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/unpacking.py
        :language: python3


**💡 learnt from:**

* Source: `Raymond Hettinger`_
* Reference: `Transform Python Slides`_

.. _Raymond Hettinger: https://github.com/rhettinger
.. _Transform Code into Beautiful, Idiomatic Python: https://www.youtube.com/watch?v=OSGv2VnC0go>
.. _Transform Python Slides: https://speakerdeck.com/pyconslides/transforming-code-into-beautiful-idiomatic-python-by-raymond-hettinger-1
