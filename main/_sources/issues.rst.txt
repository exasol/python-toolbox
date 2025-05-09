.. _issue_tracking:

:octicon:`list-unordered` Issue Tracking Guide
==============================================

Summary
+++++++
Issue tracking is a great tool to track pending work and improve the overall communication within a project.
But similar to every other tool, it needs to be used with care.

    | "A fool with a tool is still a fool"
    | -- Grady Booch

This guide will try to help you to get the best out of the issue tracking for you, your teammates and the project(s)
you are working on, by answering the following questions:

* When to create an issue?
* What makes a good issue?
* How to maintain an issue?

When to create an issue?
++++++++++++++++++++++++
Let me start by saying there is no perfect and one size fits all ruleset to decide this question, otherwise there would be some code doing that for us.
The good thing though is, humans are great in dealing with fuzzy problems. Still most people want to have something to orient themselves.
Asking more specific questions often helps in this situation.

The following question(s), helped us in the past, to get a better handle on this:

* What is the cost/benefit ratio of creating an issue?
    * cost being mainly time and effort
    * benefit being the upsides we gain from having an issue

* What is the signal to noise ratio?
    * signal being the actual code/change bringing some benefit/value to the project
    * noises being the overhead

* Is the user (api or product) impacted by this change?
    * Is it an "internal improvement" quality of life and/or code quality


Examples
--------
Fixing a couple of typos
________________________
You stumble upon a couple of typos in a Project.

Possible Action(s)
~~~~~~~~~~~~~~~~~~
* You fix the typos without creating an issue

Suspicious amount of typos
___________________________
You stumble upon a various typos within a piece of documentation you are reading. Because of the vast amount
of typos and the overall structure you expect the whole documentation to contain a substantial amount of typos.

Possible Action(s)
~~~~~~~~~~~~~~~~~~
* If the documentation is not to big and you can make the time to fix the typos right away without creating an issue.
* If the documentation is quite big, and fixing this e.g. would take you more than 1/2 a day you definitely should create an issue.
* You are unsure how long it will take to address and check the documentation and you currently can't spent time for detours create an issue.

What makes a good issue
+++++++++++++++++++++++

    **TL;DR:** An good issue describes a piece of work, it's context and it's assumption in a way, any person capable of working
    on the project, can understand it, based on the information referenced and within the issue.

To begin with, we want to make sure you understand that creating good a issue is not a zero effort action. Various things
like issue templates, can remove tedious boilerplate work, but still creating a good issue is some actual work.
It is crucial to have well crafted issues, because bad issues do way more harm than good. So let's take a step
back and let's think about why we need to have good issues, in order to better understand what actually makes a good issue.

Boiled down to it's core issue tracking is just a list of pieces of work which are needed to be done.
This list in turn, then can be used to plan, organize and track "progress/work".

Broken down to an individual issue, this means an issue should provide all relevant information about
a "single" piece/unit of work.

Even though the part what an issue is about is well understood, by most people, this is also where it goes wrong.

**Why?** Because we as humans tend to use and assume context implicitly. Assuming context implicitly already can be a problem
when communicating with people we meet on a regular basis, but is a huge problem when you communicate with people which
we meet rarely or even never.

This is somewhat obvious when you think about the fact that 60-70 % of human communication is non verbal communication.
This most likely also part of the reason so many people use emojies, a picture says more than a 1000 words
and therefore can help transport context more easily 😉. But even those helpers aren't perfect and it very
often depends on the mood and the other persons perception (context) of you how they interpret a specific emoji you have sent.

To take on a more computer science specific example:

.. list-table:: **TL;DR: Context matters**
    :header-rows: 1

    * - Information
      - Context
      - Value
    * - 65
      - ASCII
      - 'A'
    * - 65
      - Hex
      - 101
    * - 65
      - Decimal
      - 65


As you may have realized by know our point being how information is understood and processed highly depends on the context.

To come back now to the topic of **"What makes a good issue"**, a major part of it is to make context and assumptions
an explicit part of your information you are providing. Write the issue in such a way, that a person
working on the project, now or in the future can precisely understand the task, the context and assumptions
of it.


.. attention::

    You may inclined to think, you gonna address this task anyway or it is just for "your" book keeping,
    but then this is nothing for the issue tracker rather something for your personal todo list.
    If you decide it is important enough for the issue tracker than treat it as such.


**So what does this mean in more practical actionable terms?**

* Make your context explicit
        - Add links and references to spec you may already know
        - Add information e.g. from discussion, meetings, mails ...

* Make your assumptions explicit
        - Write them down also note e.g. if you are not sure if it is the right decision but what you have taken into account at the point in time when you wrote it down

* Add SubTasks regarding "standard" processes which people may not necessarily know about
      - This can be simplified e.g. by providing issue templates
      - update documentation
      - update changelog
      - ...

* Make it easy to answer the following questions for the person working/reading the issue
      - Is this issue still relevant, or is it obsolete by now?
      - Are the assumptions still valid today?
      - Did they have more or less context than we have today?
      - Did I consider the assumptions and context of the one writing the issue?


.. attention::

    More details on a specific issue type you will find in the corresponding subsection(s) of this guide.


How to maintain an issue
++++++++++++++++++++++++
As you already know an issue does not only keep track of what needs to be done, but also about it's context (how, why, etc.).
This context can be a quite dynamic though, especially for tasks which bare a larger amount of uncertainty (e.g. bugs).
So a huge part of keeping an issue up to date, is keep updating it's context. The following scenarios will
try to give you an idea on how to update and maintain an issue in various scenarios.

TL;DR
-----

* Keep the issue and it's context up to date
    * Keep the status up to date [Backlog, In Progress, ...]
    * Update tickets which are actively worked on regularly (at least every 2-3 days)
    * Try to communicate new information via comments (e.g. status update's)
    * Report important changes because of internal and external events

* Comments
    * Respond to comments in a timely manner
    * Stay friendly and focused on the issue when responding to comments



Scenarios
---------

A developer picks up the issue from the backlog and starts working on it
________________________________________________________________________

* Assign the ticket to the developer working on it
* Change the state of the issue to "In Progress"

    .. note::

        Most issue tracking system already take care of this if you move it
        to the appropriate category in the issue(s) overview.

The Issue Receives a comment
____________________________

* Make sure to reply to a comment in a timely manner
* If it is the first contribution/comment of the contributor on this issue, show appreciation for the contribution.
    * If the comment can't be addressed right away, at least acknowledge the comment and communicate some timeframe
* Make sure the comment can be understood in the context of the issue
    * If needed ask for clarification
    * If needed ask follow up questions
* Be clear in your response(s)
    * Make sure relevance, importance, course of action and timeframe are communicated if necessary

The Developer stop's/postpones working on the issue, e.g. due to re prioritization
__________________________________________________________________________________

* Remove assignee on the ticket
* Change the state of the issue to "Backlog"

    .. note::

        Most issue tracking system already take care of this if you move it
        to the appropriate category in the issue(s) overview.

* Make sure all current context information is updated or added as status comment to the issue
* Add information about why working on the issue have been postponed/stopped (e.g. blocked)
    * Except if this would disclose information to the wrong audience
* Communicate when work on the issue will be picked up again
    * Communicating that it is unclear when the work will be continued, is also fine

Stalled issue (e.g. root cause of bug is hard to find)
______________________________________________________

.. note::

    Very rarely the issue (work) is really stalled, often it just feels like this.
    When you can't report on explicitly achieved task(s), provide context information
    about your work (journey). This can help you and others to pickup on it latter
    or at least it help to understand the current state more clearly.

* Regularly post a status update on the issue (every 2-3 days)
    * What issues/problems already have been ruled out and why?
    * What is the current strategy to find the culprit?
    * What is the current strategy to resolve roadblocks?
    * What are the current assumptions and hunches?
    * Are there any further leads to be investigated in the future?
    * Describe the current roadblocks
    * Report sub partial successes
    * Add script's and context information which helps to reproduce and/or trigger the bug


**Example:** Status Update on Bug Issue

.. code-block:: markdown

    # Status Update
    Further investigation's have shown that the basic SQLA test suite mostly is intact after the upgrade to `1.4` (14 failures), when run in "isolation". Various exasol specific test suites:

       * test/test_get_metadata_functions.py
       * test/test_large_metadata.py
       * test/test_regression.py (TranslateMap)

    seem to have negative side effects which cause 100+ tests to  :boom: fail/crash, if run after those test suites.
    This further strengthens the case for the **assumptions** mentioned in the previous update:

       * Setup/Teardown mechanic of `testing.fixtures.TablesTest` has changed
       * Setup/Teardown mechanic fails due to leftovers in tests DB

    Also, this narrows down the potential root cause(s).

    ## Remark(s)
    Common to all those test suites to be that they add/remove schemas.
    For `test/test_regression.py` it have been proven that the schema manipulating test (`TranslateMap`) causes some negative side effect on following test suits.

    ## Notes & Ideas (from discussion with @tkilias )
    * Is schema inference still working correctly?
    * Does the "disabled" caching cause side effects?
    * Do implicit schema open and closes affect the current schema for follow up tests?

    ## Next Steps
    * Analyze effects of implicit open/close of schema(s)
    * A more in depth analysis regarding side effects and cleanup of the mentioned test suites will be done

To see the example update in it's full context look `here <https://github.com/exasol/sqlalchemy-exasol/issues/106#issuecomment-1245305351>`_.
