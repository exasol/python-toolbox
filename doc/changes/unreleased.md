# Unreleased

## Summary

### Links in the Documentation 
This version of the PTB adds nox tasks to check links present in our documentation:

    docs:link - List all the links within the documentation
    docs:links:check - Checks whether all links in the documentation are accessible

`docs:links:check` is run in the CI `checks.yml`. If this step fails in the CI,
please check the output & manually resolve the issues. There might be some cases
where you need to update your doc/conf.py with specific values for the allowed
options for the Linkcheck Builder.

We recommend the following values be added:

    linkcheck_rate_limit_timeout = 40
    linkcheck_timeout = 10
    linkcheck_delay = 20
    linkcheck_retries = 2
    linkcheck_anchors = False
    linkcheck_ignore: list[str] = []
    linkcheck_allowed_redirects = {
        # All HTTP redirections from the source URI to
        # the canonical URI will be treated as "working".
        r"https://github\.com/.*": r"https://github\.com/login*"
    }

## ✨ Features
* #409: Doc link & checks

## Refactoring
* Switched deprecated Pydantic class-based `config` to `ConfigDict`

## Security
* #477: Switched `sonar:check` to use `SONAR_TOKEN` from the environment
