# 1.7.2 - 2025-07-31

# Summary

GPU runners throughout our various Python repositories were breaking due to underlying
changes in the runners. This affected the usage of the `python-environment/action`,
and it could be resolved by adding `--break-system-packages` to the `pip install`
command. The behavior then is to default to the user installation, which avoids
the global issues the GPU runners were running into.

# Bugfix

* Modified pip install statement to include --break-system-packages
