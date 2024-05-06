import pluggy

_PLUGIN_MARKER = "python-toolbox"
hookspec = pluggy.HookspecMarker("python-toolbox")
hookimpl = pluggy.HookimplMarker("python-toolbox")


class NoxTasks:
    @hookspec
    def prepare_release_update_version(self, session, config, version):
        """
        Run as part of the version update task

        Args:
            session:
                tbd
            config:
                tbd
            version:
                tbd
        """

    @hookspec
    def prepare_release_add_files(self, session, config, add):
        """
        Files which should be added to the prepare relase commit should be added using add.

        Args:
            add: Function which takes a file which will be added to the index.
        """

    @staticmethod
    def plugin_manager(config) -> pluggy.PluginManager:
        pm = pluggy.PluginManager(_PLUGIN_MARKER)
        pm.add_hookspecs(NoxTasks)
        for plugin in config.plugins:
            pm.register(plugin())
        return pm
