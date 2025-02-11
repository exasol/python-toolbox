How to Release
==============

#.  Use the command :code:`nox -s release:prepare` to prepare the project for a new release.
#.  Merge your **Pull Request** to main
#.  Switch the **current branch** to the **default branch**
#.  Ensure default branch to be up to date: :code:`git pull`
#.  Set your **tag name**: :code:`TAG=<name>`
#.  Use :code:`git tag "${TAG}"` to create a new tag in your repo
#.  Use :code:`git push origin "${TAG}"` to push it in your remote repo
#.  GitHub workflow reacts on this tag and starts the release process