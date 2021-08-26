Maintainer Guide
================

This is a guide for buildtest maintainers


Incoming Pull Request
------------------------

These are just a few points to consider when dealing with incoming pull requests

1. Any incoming Pull Request should be assigned to one or more maintainers for review.

2. Upon approval, the PR should be **Create a merge commit** or **Squash and merge** depending on your preference. To preserve commit history please use **Create a merge commit** though sometimes it can be useful to do Squash commit. For more details on merge request see https://docs.github.com/en/github/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request

3. Maintainers can request user to put meaningful commit if author has not provided a meaningful message (i.e ``git commit --amend``)

4. Maintainers are requested that committer name and email is from a valid Github account. If not please request the committer to fix the author name and email.

5. All incoming PRs should be pushed to `devel <https://github.com/buildtesters/buildtest/tree/devel>`_ branch, if you see any PR sent to any other branch please inform code owner to fix it


Release Process
-----------------

Every buildtest release will be tagged with a version number using format **X.Y.Z**. Every release will have a tag that corresponds
to a release such as ``v1.2.3``. Git tags should be pushed to upstream by **release manager** only.
The process for pushing git tags can be described in the following article:  `Git Basics - Tagging <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_

We will create annotated tags as follows::

  git tag -a v1.2.3 -m "buildtest version 1.2.3"

Once tag is created you can view the tag details by running either::

  git tag
  git show v1.2.3

We have created the tag locally, next we must push the tag to the upstream repo by doing the following::

  git push origin v.1.2.3

Every release must have a release note that is maintained in file `CHANGELOG.rst <https://github.com/buildtesters/buildtest/blob/master/CHANGELOG.rst>`_

Under buildtest `releases <https://github.com/buildtesters/buildtest/releases>`_ a new release can be created that
corresponds to the git tag. In the release summary, just direct with a message stating **refer to CHANGELOG.rst for more details**

Once the release is published, make sure to open a pull request from ``devel`` --> ``master`` and **Rebase and Merge**
to master branch. If there are conflicts during merge for any reason, then simply remove ``master`` and create a master
branch from devel.

Default Branch
------------------

The default branch is `devel <https://github.com/buildtesters/buildtest/tree/devel>`_ and this should be `protected branch <https://docs.github.com/en/github/administering-a-repository/defining-the-mergeability-of-pull-requests/about-protected-branches>`_.

Branch Settings
----------------

All maintainers are encouraged to view branch `settings <https://github.com/buildtesters/buildtest/settings/branches>`_
for ``devel`` and ``master``. If something is not correct please consult with the maintainers.

The master and devel branches should be protected branches and master should be enabled as default branch. Shown
below is the expected configuration.

.. image:: buildtest_branch_settings.png

Merge Settings
----------------

We have enabled all commit types i.e (merge commits, squash merging, rebase merging) for merging Pull Request.  Shown below is the
recommended configuration, if you see a deviation please inform the maintainers.

.. image:: buildtest_merge_options.png

If you notice a deviation, please consult with the maintainers.

Google Analytics
-----------------

The buildtest site is tracked via Google Analytics, if you are interested in get access contact **Shahzeb Siddiqui** `@shahzebsiddiqui <https://github.com/shahzebsiddiqui/>`_

Read The Docs Access
---------------------

buildtest project for readthedocs can be found at https://readthedocs.org/projects/buildtest/. If you need
to administer project configuration, please contact **Shahzeb Siddiqui** `@shahzebsiddiqui <https://github.com/shahzebsiddiqui/>`_ to gain access.

Slack Admin Access
-------------------

If you need admin access to Slack Channel please contact **Shahzeb Siddiqui** `@shahzebsiddiqui <https://github.com/shahzebsiddiqui/>`_. The
slack admin link is https://hpcbuildtest.slack.com/admin
