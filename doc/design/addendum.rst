Addendums and Updates
=====================

Nox as Task Executor and Task Creation
--------------------------------------

Why Nox Was Chosen
~~~~~~~~~~~~~~~~~~

Nox was initially selected as our task executor due to several reasons:

* **No Additional Languages Required**: There was no need to introduce extra programming languages or binaries, simplifying the development process.
* **Python-based**: Being Python-based, Nox can be extended, understood by python devs and also can share code.
* **Simplicity**: Nox is relatively "small" in functionality which makes it somewhat simple to use.

Although today, other options like `invoke` could be consider or used as a replacement, Nox still is working for use even though there are some rough edges.

Naming of Tasks and Grouping
----------------------------

Task Grouping with Nox
~~~~~~~~~~~~~~~~~~~~~~

Since Nox doesn't natively support task grouping like Invoke, we need a strategy to clearly distinguish commands. We will adopt a naming convention to indicate grouping within the CLI. 

Groups will be separated using a :code:`:` (colon) because :code:`-` (dash) might already be used within task names.

Examples
++++++++

**Task Names:**

* :code:`docs:clean`
* :code:`docs:build`
* :code:`docs:open`


**CLI Execution:** :code:`nox -s docs:clean docs:build docs:open`

This approach helps in organizing tasks logically and makes it easier for developers to identify and execute related commands.

By following these guidelines, we ensure a structured and comprehensible task management system, facilitating smoother development and maintenance.
