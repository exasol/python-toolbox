import pluggy

_PLUGIN_MARKER = "python-toolbox"
hookspec = pluggy.HookspecMarker("python-toolbox")
hookimpl = pluggy.HookimplMarker("python-toolbox")


class NoxTasks:
    """
    Defines extension hooks for the standard nox tasks provided by the python-toolbox.
    """

    @hookspec
    def prepare_release_update_version(self, session, config, version):
        """
        This hook is called during version updating when a release is being prepared.
        Implementors can add their own logic and tasks required to be run during the version update here.

        Args:
            session (nox.Session):
                The nox session running the release preparation.
                This it can be used to run commands, etc.

            config (class):
                The project configuration object from the noxconfig.py file.

            version (str):
                A string representation of the version to be released.
                This follows the pattern of Semantic Versioning, i.e., "MAJOR.MINOR.PATCH".
                An example would be "1.4.2".
        """

    @hookspec
    def prepare_release_add_files(self, session, config):
        """
        Files which should be added to the prepare relase commit should be added using add.

        Args:
            session (nox.Session):
                The nox session running the release preparation.
                This it can be used to run commands, etc.

            config (class):
                The project configuration object from the noxconfig.py file.

        Return:
            A iterable of Path objects of files to be added.

            e.g.:  [Path("file1.txt")] or [Path("file1.txt"), Path("file2.txt")]
        """

    @staticmethod
    def plugin_manager(config) -> pluggy.PluginManager:
        pm = pluggy.PluginManager(_PLUGIN_MARKER)
        pm.add_hookspecs(NoxTasks)
        for plugin in getattr(config, "plugins", []):
            pm.register(plugin())
        return pm
