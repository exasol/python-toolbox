# Good
from collections import ChainMap

cli_args = {"user": "FooBar", "cmd": "ls -all"}
env_args = {"user": "Johndoe"}
cfg_args = {"user": "default", "cwd": "/home/default", "cmd": "ls"}

config = ChainMap(cli_args, env_args, cfg_args)

# Bad
cli_args = {"user": "FooBar", "cmd": "ls -all"}
env_args = {"user": "Johndoe"}
cfg_args = {"user": "default", "cwd": "/home/default", "cmd": "ls"}

config = {}
config.update(cfg_args)
config.update(env_args)
config.update(cli_args)
