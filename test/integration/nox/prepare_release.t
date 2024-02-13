Test prepare-release nox target

Setup
========================================================= 

  $ cat > noxfile.py <<EOF
  > """defines nox tasks/targets for this project"""
  > import nox
  > 
  > from exasol.toolbox.nox.tasks import prepare_release
  > EOF


prepare-release without version should fail
========================================================= 

  $ nox -s prepare-release
  nox > Running session prepare-release
  usage: nox -s prepare-release -- [-h] version
  nox -s prepare-release: error: the following arguments are required: version
  [2]


prepare-release with invalid version format should fail
========================================================= 

  $ nox -s prepare-release -- 1.B.0
  nox > Running session prepare-release
  usage: nox -s prepare-release -- [-h] version
  nox -s prepare-release: error: argument version: Expected format: <number>.<number>.<number>, e.g. 1.2.3, actual: 1.B.0
  [2]


print prepare-release help
========================================================= 

  $ nox -s prepare-release -- -h
  nox > Running session prepare-release
  usage: nox -s prepare-release -- [-h] version
  
  positional arguments:
    version     A version string of the following format:"NUMBER.NUMBER.NUMBER"
  
  option*: (glob)
    -h, --help  show this help message and exit

