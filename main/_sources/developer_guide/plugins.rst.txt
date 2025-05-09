.. _plugin support:

Plugin Support
==============

Our tool currently provides plugin support for Nox tasks. The plugins dedicated to Nox tasks can be found
within the :code:`exasol.toolbox.nox.plugins` namespace. To facilitate the implementation of this feature,
we utilize `pluggy <https://pluggy.readthedocs.io/en/stable/>`_, an extensible plugin system for Python.
At present, our usage of `pluggy` is confined to a selection of its capabilities.
We mandate that plugins define and implement hooks, following which they must register their hook
implementations with the configuration object.
For more information on hook configuration, refer to the :ref:`plugins` section in our User Guide.

It is essential for plugins to operate without raising exceptions. Plans are in place to handle exceptions more robustly in future releases.
This entails capturing and logging any exceptions raised within the plugins, without disrupting the continued execution of the task at hand.
The only exception to this rule applies to instances derived from `nox.error`, which are handled as specified.
For additional insights into the handling of plugin exceptions, review the section on
`hook wrappers <https://pluggy.readthedocs.io/en/stable/#wrappers>`_ in the `pluggy` documentation.
