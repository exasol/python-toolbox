Customization
=============

.. _plugins:

Nox Task Plugins
----------------

Some Nox tasks allow for implementing custom hooks to be executed within the Nox workflow.
To ensure a predictable environment, plugins should be written to handle exceptions gracefully.
If a plugin encounters a critical situation where it cannot continue execution, it should call the ``error``
method on the session object, effectively halting the execution process.
This action may have a widespread impact by forcibly stopping execution, potentially affecting other plugins and code paths.

.. attention:: Doing a hard exit using ``session.error`` should be an measure of last resort.

.. note::

    Even though the plugin mechanism utilizes `pluggy <https://pluggy.readthedocs.io/en/stable/>`_ under the hood, it does
    not currently support all scenarios and features with which one may be familiar from pytest, or other tools and
    frameworks based on pluggy. Nevertheless, a look at pluggy's `documentation <https://pluggy.readthedocs.io/en/stable/>`_
    can definitely enhance understanding of the hook mechanism.


Implementing Plugins
~~~~~~~~~~~~~~~~~~~~

To create a Nox plugin, the hooksimpl decorator must be imported from the Nox plugin infrastructure:

.. code-block:: python

    from exasol.toolbox.nox.plugin import hookimpl

You can then define a class with methods decorated with ``@hookimpl`` to specify the hooks that the plugin implements.
The class should be instantiable without any arguments, however, you may include class attributes and provide alternative means for customization.

Here is an example plugin that updates templates as part of release preparation:

.. code-block:: python

    from exasol.toolbox.nox.plugin import hookimpl

    class UpdateTemplates:

        def __init__(self):
            self.workflows = [...]

        @hookimpl
        def prepare_release_update_version(self, session, config, version):
            for workflow in self.workflows:
                self.update_workflow(workflow, version)

        @hookimpl
        def prepare_release_add_files(self, session, config):
            return self.workflows

        def update_workflow(self, workflow, version):
            # update the workflow with the new version
            pass

.. note:: The above `update_workflow` method is a non-hook utility method within the class.

Plugin Registration
~~~~~~~~~~~~~~~~~~~

Once the plugin class has been defined, it must be registered in the Nox configuration. This is done by adding the class to the `plugins` list within the `Config` data class.

In the Nox `Config` data class, you should amend the `plugins` list to include the new plugin:

.. code-block:: python

    @dataclass(frozen=True)
    class Config:
        """Project-specific configuration used by Nox infrastructure."""
        # ... other configuration attributes ...

        plugins = [UpdateTemplates]  # register the plugin

When Nox runs, it will instantiate `UpdateTemplates` with no arguments and integrate the hooks defined by the plugin into the execution lifecycle. All registered plugins’ hooks are called at their designated points in the Nox workflow.

Always remember to follow the plugin development guidelines to ensure that your plugin is robust and integrates well with Nox and other potential plugins.
