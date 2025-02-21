How to Release?
===============

#.  Use :code:`TAG=<name>` to set a variable named **"TAG"**
#.  Use :code:`nox -s release:prepare -- ${TAG}` to prepare the project for a new release.
#.  Merge your **Pull Request** to the **default branch**
#.  Use :code:`git remote show origin | sed -n '/HEAD branch/s/.*: //p'` to output the **default branch**
#.  Use :code:`git checkout <default branch>` Switch to the **default branch**
#.  Use :code:`git pull` to update branch
#.  Use :code:`git tag "${TAG}"` to create a new tag in your repo
#.  Use :code:`git push origin "${TAG}"` to push it to remote
#.  GitHub workflow **CD** reacts on this tag and starts the release process