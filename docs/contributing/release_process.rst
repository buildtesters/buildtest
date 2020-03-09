Maintainer Guide
================

Incoming Pull Request
------------------------

Any incoming Pull Request should be assigned to one or more maintainers for review. Upon approval, the PR should
be **Squash and Merge**. If it's important to preserve a few commits during PR then **Rebase and merge** is acceptable.

Release Process
-----------------

Every buildtest release will be tagged with a version number using format **X.Y.Z**. Every release will have a git tags
such as ``v1.2.3`` to correspond to release **1.2.3**. Git tags should be pushed to upstream by **release manager** only.
The process for pushing git tags can be described in the following article:  `Git Basics - Tagging <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_

We will create annotated tags as follows::

  git tag -a v1.2.3 -m "buildtest version 1.2.3"

Once tag is created you can view the tag details by running either::

  git tag
  git show v1.2.3

We have created the tag locally, next we must push the tag to the upstream repo by doing the following::

  git push origin v.1.2.3

Every release must have a release note that is maintained in file `CHANGELOG.rst <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/CHANGELOG.rst>`_

Under buildtest `releases <https://github.com/HPC-buildtest/buildtest-framework/releases>`_ a new release can be created that
corresponds to the git tag. In the release summary, just direct with a message stating **refer to CHANGELOG.rst for more details**
