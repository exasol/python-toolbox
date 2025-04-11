Separation of Concerns
----------------------

Filters
+++++++

.. tab:: ✅ With Filter

    .. literalinclude:: ../../../_static/idioms/filters.py
        :language: python3
        :start-after: # With Filter
        :end-before: # Naive Approach

.. tab:: ❌ Naive Approach

    .. literalinclude:: ../../../_static/idioms/filters.py
        :language: python3
        :start-after: # Naive Approach

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/filters.py
        :language: python3


Adapters
++++++++

.. tab:: ✅ With Adapter

    .. literalinclude:: ../../../_static/idioms/adapter.py
        :language: python3
        :start-after: # With Adapter
        :end-before: # Naive Approach

.. tab:: ❌ Naive Approach

    .. literalinclude:: ../../../_static/idioms/adapter.py
        :language: python3
        :start-after: # Naive Approach

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/adapter.py
        :language: python3


**💡 learnt from:**

* Source: `Will McGugan`_
* Reference: `Stealing Open Source code from Textual`_

    `Adapter's used in textual <https://github.com/Textualize/textual/blob/d2ba22b86f48f4ce5b0f55767efdcf1a5478b180/src/textual/_loop.py>`_

    .. tab:: loop_first

        .. code-block:: python

            from __future__ import annotations

            from typing import Iterable, TypeVar

            T = TypeVar("T")


            def loop_first(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
                """Iterate and generate a tuple with a flag for first value."""
                iter_values = iter(values)
                try:
                    value = next(iter_values)
                except StopIteration:
                    return
                yield True, value
                for value in iter_values:
                    yield False, value


    .. tab:: loop_last

        .. code-block:: python

            from __future__ import annotations

            from typing import Iterable, TypeVar

            T = TypeVar("T")


            def loop_last(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
                """Iterate and generate a tuple with a flag for last value."""
                iter_values = iter(values)
                try:
                    previous_value = next(iter_values)
                except StopIteration:
                    return
                for value in iter_values:
                    yield False, previous_value
                    previous_value = value
                yield True, previous_value


    .. tab:: loop_first_last

        .. code-block:: python

            from __future__ import annotations

            from typing import Iterable, TypeVar

            T = TypeVar("T")


            def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
                """Iterate and generate a tuple with a flag for first and last value."""
                iter_values = iter(values)
                try:
                    previous_value = next(iter_values)
                except StopIteration:
                    return
                first = True
                for value in iter_values:
                    yield first, False, previous_value
                    first = False
                    previous_value = value
                yield first, True, previous_value


Short-Circuit Search
++++++++++++++++++++

.. tab:: ✅ Good

    .. literalinclude:: ../../../_static/idioms/short_circuit.py
        :language: python3
        :start-after: # With Generator Short Circuit
        :end-before: # Naive Approach

.. tab:: ❌ Bad

    .. literalinclude:: ../../../_static/idioms/short_circuit.py
        :language: python3
        :start-after: # Naive Approach

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/short_circuit.py
        :language: python3


Generic Solution
________________

.. code-block:: python

    from typing import Iterator, Any, Callable, TypeVar

    T = TypeVar('T')


    def find_first(
            iterable: Iterator[T],
            condition: Callable[[T], bool],
            terminal: Any = None
    ) -> Any:
        """
        Find the first item which meets a specific condition.

        Args:
            iterable:
                which will be searched.
            condition:
                which needs to be meet by the item.
            terminal:
                value which will be returned if the condition did not return True
                for any item in the iterable.

        Returns:
            The first item in the iterable for which the condition returns True.
            If the condition does not return True for any item in the iterable, the
            terminal value is returned.

        Examples:

        >>> numbers = [1, 2, 3, 4 ,5 ,6]
        >>> value = find_first(numbers, condition=lambda _: True)
        >>> value == 1
        True

        >>> numbers = [1, 2, 3, 4 ,5 ,6]
        >>> value = find_first(numbers, condition=lambda item: item % 3 == 0)
        >>> value == 3
        True

        >>> value = find_first(numbers, condition=lambda item: item % 7 == 0)
        >>> value is None
        True

        >>> value = find_first(numbers, condition=lambda item: item % 7 == 0, terminal=7)
        >>> value == 7
        True
        """
        items = (item for item in iterable if condition(item))
        try:
            item = next(items)
        except StopIteration:
            item = terminal
        return item

Context Manager
+++++++++++++++
Factor out context into a context manager.

.. tab:: ✅ With Context Manager

    .. tab:: Python 3.8 - 3.10

        .. literalinclude:: ../../../_static/idioms/context_manager.py
            :language: python3
            :start-after: # With Context Manager
            :end-before: # With Python 3.11

    .. tab:: Python 3.11

        .. literalinclude:: ../../../_static/idioms/context_manager.py
            :language: python3
            :start-after: # With Python 3.11
            :end-before: # Naive Approach

.. tab:: ❌ Naive Approach

    .. literalinclude:: ../../../_static/idioms/context_manager.py
        :language: python3
        :start-after: # Naive Approach

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/context_manager.py
        :language: python3


**💡 learnt from:**

* Source: `Raymond Hettinger`_
* Reference: `Transform Python Slides`_

Decorator
+++++++++
Factor out unrelated repetitive work into a decorator.

.. tab:: ✅ With Decorator

    .. literalinclude:: ../../../_static/idioms/context_decorator.py
        :language: python3
        :start-after: # With Decorator
        :end-before: # Naive Approach

.. tab:: ❌ Naive Approach

    .. literalinclude:: ../../../_static/idioms/context_decorator.py
        :language: python3
        :start-after: # Naive Approach

.. tab:: 🎭 Compare

    .. literalinclude:: ../../../_static/idioms/context_decorator.py
        :language: python3


.. _Raymond Hettinger: https://github.com/rhettinger
.. _Will McGugan: https://github.com/willmcgugan
.. _Transform Code into Beautiful, Idiomatic Python: https://www.youtube.com/watch?v=OSGv2VnC0go>
.. _Transform Python Slides: https://speakerdeck.com/pyconslides/transforming-code-into-beautiful-idiomatic-python-by-raymond-hettinger-1
.. _Stealing Open Source code from Textual: https://textual.textualize.io/blog/2022/11/20/stealing-open-source-code-from-textual/
