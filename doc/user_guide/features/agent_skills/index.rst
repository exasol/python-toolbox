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

These shared checks are intentionally separate from skill-specific tests. The
test suite validates the structure of every packaged skill and validates the
structure of every available ``eval_cases.yml``. When adding a skill, add its
expected files and behavior assertions to the shared skill test patterns.

Installing packaged skills
---------------------------

Projects can install all skills packaged by their current PTB dependency with:

.. code-block:: shell

    poetry run -- nox -s skills:install

The session copies each packaged skill into its own directory below
``.agents/skills``. Existing files in those skill directories are replaced so
the installed copies stay aligned with the PTB version.
