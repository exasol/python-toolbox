import pluggy

_PLUGIN_MARKER = "python-toolbox-nox"
hookspec = pluggy.HookspecMarker("python-toolbox-nox")
hookimpl = pluggy.HookimplMarker("python-toolbox-nox")


class NoxTasks:
    """
    Defines extension hooks for the standard Nox tasks provided by the python-toolbox.

    This class provides an interface that allows various actions to be taken
    when certain events occur within the Nox task execution environment.
    Examples of such events are: the start of a task or the end of a task.

    In Plugins, exceptions should not be thrown. Instead, use the `error` method on the session
    object to abort task execution. However, keep in mind that forcefully stopping execution
    could potentially impact any other code that depends on the execution of the aborted task.
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

            config (object):
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

            config (object):
                The project configuration object from the noxconfig.py file.

        Return:
            A iterable of Path objects of files to be added.

            e.g.:  [Path("file1.txt")] or [Path("file1.txt"), Path("file2.txt")]
        """

    @hookspec
    def pre_integration_tests_hook(self, session, config, context):
        """
        Implement if project specific behaviour is required before running integration tests.

        This function acts as a hook that gets called before the execution of integration tests.
        It can be used to execute any project-specific tasks that need to be performed before
        the tests run, such as starting or initalizing a database.

        Args:
            session (nox.Session):
                The nox session that ran the integration tests.
                It can be used to run additional commands, etc.

            config (object):
                The project's configuration object from the noxconfig.py file.

            context (dict):
                Contains additional contextual information related to the testing session.
                All keys in this dictionary will be strings, while the values can be of any type.
        """

    @hookspec
    def post_integration_tests_hook(self, session, config, context):
        """
        Implement if project specific behaviour is required after running integration tests.

        This function acts as a hook that gets called after the execution of integration tests.
        It can be used to execute any project-specific tasks that need to be performed after
        the tests run, such as clean up, data processing, reporting etc.

        Args:
            session (nox.Session):
                The nox session that ran the integration tests.
                It can be used to run additional commands, etc.

            config (object):
                The project's configuration object from the noxconfig.py file.

            context (dict):
                Contains additional contextual information related to the testing session.
                All keys in this dictionary will be strings, while the values can be of any type.
        """

    @staticmethod
    def plugin_manager(config) -> pluggy.PluginManager:
        pm = pluggy.PluginManager(_PLUGIN_MARKER)
        pm.add_hookspecs(NoxTasks)
        for plugin in getattr(config, "plugins", []):
            pm.register(plugin())
        return pm
