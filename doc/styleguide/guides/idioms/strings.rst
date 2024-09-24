Strings
-------

Concatenation
+++++++++++++
Use *.join* to to concatenate strings

.. tab:: ✅ Good

    .. literalinclude:: ../../../_static/idioms/concat.py
        :language: python3
        :start-after: # Good
        :end-before: # Bad

.. tab:: ❌ Bad

    .. literalinclude:: ../../../_static/idioms/concat.py
        :language: python3
        :start-after: # Bad

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/concat.py
        :language: python3


**💡 learnt from:**

* Source: `Raymond Hettinger`_
* Reference: `Transform Python Slides`_

f-Strings
+++++++++
Use f-String for simple placeholder expressions

.. tab:: ✅ Good

    .. literalinclude:: ../../../_static/idioms/fstring.py
        :language: python3
        :start-after: # Good
        :end-before: # Bad

.. tab:: ❌ Bad

    .. literalinclude:: ../../../_static/idioms/fstring.py
        :language: python3
        :start-after: # Bad

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/fstring.py
        :language: python3


String.format
+++++++++++++
Use the string format function for complex expressions

.. tab:: ✅ Good

    .. literalinclude:: ../../../_static/idioms/format.py
        :language: python3
        :start-after: # Good
        :end-before: # Bad

.. tab:: ❌ Bad

    .. literalinclude:: ../../../_static/idioms/format.py
        :language: python3
        :start-after: # Bad

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/format.py
        :language: python3


**💡 learnt from:**

* Source: `Robert Smallshire`_ , `Austin Bingham`_
* References: `Rober Smallshire - Courses`_, `Austin Bingham - Courses`_

.. _Raymond Hettinger: https://github.com/rhettinger
.. _Austin Bingham: https://leanpub.com/u/abingham
.. _Robert Smallshire: https://leanpub.com/u/robert-smallshire

.. _Transform Code into Beautiful, Idiomatic Python: https://www.youtube.com/watch?v=OSGv2VnC0go>
.. _Transform Python Slides: https://speakerdeck.com/pyconslides/transforming-code-into-beautiful-idiomatic-python-by-raymond-hettinger-1
.. _Austin Bingham - Courses: https://www.pluralsight.com/authors/austin-bingham
.. _Rober Smallshire - Courses: https://www.pluralsight.com/authors/robert-smallshire
