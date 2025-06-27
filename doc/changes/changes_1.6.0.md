# 1.6.0 - 2025-06-27

## Summary

### Links in the Documentation 
This version of the PTB adds nox tasks to check links present in our documentation:

    links:list - List all the links within the documentation
    links:check - Checks whether all links in the documentation are accessible

`links:check` is run in the CI `checks.yml`. If this step fails in the CI, it will cause
the build to break. Please check the output & manually resolve the issues. There might
be some cases where you need to update your `doc/conf.py` with specific values for the allowed
options for the [Linkcheck Builder](https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder).

We recommend the following values be added:

    linkcheck_rate_limit_timeout = 60
    linkcheck_timeout = 15
    linkcheck_delay = 30
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
