Install all workflows

  $ tbx workflow install all workflows 2>/dev/null

Check if all workflows have been installed

  $ ls workflows -1 | sort
  build-and-publish.yml
  check-release-tag.yml
  checks.yml
  ci-cd.yml
  ci.yml
  gh-pages.yml
  pr-merge.yml
  report.yml
