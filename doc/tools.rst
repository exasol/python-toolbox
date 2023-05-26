💻 Tools
========

tbox
----
The :code:`tbox` is the main entry point for all of the toolbox specific tooling.

.. code-block:: shell

     $ tbox --help

     Usage: tbox [OPTIONS] COMMAND [ARGS]...

    ╭─ Options ───────────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.             │
    │ --show-completion             Show completion for the current shell, to copy it or  │
    │                               customize the installation.                           │
    │ --help                        Show this message and exit.                           │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────╮
    │ workflow                                                                            │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯

workflow
++++++++
The workflow command helps to install and maintain GitHub workflows provided by the toolbox.

.. code-block:: shell

     $ tbox workflow --help

     Usage: tbox workflow [OPTIONS] COMMAND [ARGS]...

    ╭─ Options ───────────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                         │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────╮
    │ diff      Diff a specific workflow against the installed one.                       │
    │ install   Installs the requested workflow into the target directory.                │
    │ list      List all available workflows.                                             │
    │ show      Shows a specific workflow.                                                │
    │ update    Similar to install but checks for existing workflows and shows diff       │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯





