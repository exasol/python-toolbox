.. _agent_skills:

Agent Skills
============

The PTB can package agent skills for use by projects and provides shared
validation for their common structure and content rules.

Run the validation with:

.. code-block:: shell

    poetry run -- nox -s skills:check

The session validates every skill packaged in ``exasol.toolbox.skills``. It
checks that each skill has ``SKILL.md`` with complete frontmatter, contains no
unfinished TODO markers or forbidden repository-specific metadata, and has no
duplicated Markdown lines. Nox command examples are kept in the skill's
``references/nox-sessions.md`` file.

These shared checks are intentionally separate from skill-specific tests. When
adding a skill, add its expected files and behavior assertions to that skill's
own test module, while ``skills:check`` covers the rules common to all skills.
