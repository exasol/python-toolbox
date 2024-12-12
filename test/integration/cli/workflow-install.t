Install all workflows

  $ tbx workflow install all workflows 2>/dev/null

Check if all workflows have been installed

  $ ls workflows -1 | sort
  build-and-publish.yml
  cd.yml
  check-release-tag.yml
  checks.yml
  ci.yml
  gh-pages.yml
  matrix-all.yml
  matrix-exasol.yml
  matrix-python.yml
  merge-gate.yml
  pr-merge.yml
  report.yml
  slow-checks.yml
