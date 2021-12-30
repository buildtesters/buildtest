.. _code_contribution_guide:

Code Contribution Guide
=============================

This guide will walk through the code contribution guide, we expect you have a
:ref:`github account <github_account>` and experience using `git` and familiarity with
GitHub interface.

.. _github_account:

GitHub Account
--------------

If you don't have a GitHub account please `register <http://github.com/join>`_ your account.

Fork the repo
--------------

First, you'll need to fork the repo https://github.com/buildtesters/buildtest

You might need to setup your SSH keys in your git profile if you are using ssh option for cloning. For more details on
setting up SSH keys in your profile, follow instruction found in
https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to repository without requesting for password for every commit. Once you have forked the repo, clone your local repo::

  git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest.git


Adding Upstream Remote
-----------------------

First you need to add the ``upstream`` repo, to do this you can issue the
following::

 git remote add upstream git@github.com/buildtesters/buildtest.git

The ``upstream`` tag is used to sync changes from upstream repo to keep your
repo in sync before you contribute back.

Make sure you have set your user name and email set properly in git configuration.
We don't want commits from unknown users. This can be done by setting the following::

   git config user.name "First Last"
   git config user.email "abc@example.com"

For more details see `First Time Git Setup <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>`_

.. _sync_branches:

Sync your branch from upstream
-------------------------------

The ``devel`` from upstream will get Pull Requests from other contributors, in-order
to sync your forked repo with upstream, run the commands below::

 git checkout devel
 git fetch upstream devel
 git pull upstream devel


Once the changes are pulled locally you can sync devel branch with your
fork as follows::

 git checkout devel
 git push origin devel


Repeat this same operation with ``master`` branch if you want to sync it with
upstream repo

Contribution Workflow
----------------------

If you want to contribute back, you should create a feature branch from `devel`
and add your files, commit and push them to your fork. The workflow can be summarized
as follows::

  git checkout devel
  git checkout -b featureX
  git add <file1> <file2> ...
  git commit -m "commit message"
  git push origin featureX

Once the branch is created in your fork, you can `create a Pull Request <https://github.com/buildtesters/buildtest/compare>`_
with the destination branch ``devel`` at https://github.com/buildtesters/buildtest and base
branch which is your feature branch pushed at your fork.

.. note::
    Do not push to ``master`` or ``devel`` branch on your fork or upstream.

Pull Request Review
--------------------

Once you have submitted a Pull Request, please check the automated checks that are
run for your PR to ensure checks are passed. Most common failures in CI checks
are black and pyflakes issue, this can be done by
:ref:`configuring black <black_hook>` and running :ref:`pyflakes <using_pyflakes>`. Once all checks have passed,
maintainer will review your PR and provide feedback so please be patient.
Please coordinate with maintainer through PR or Slack.

Resolving PR Merge Conflicts
-----------------------------

Often times, you may start a feature branch and your PR get's out of sync with
``devel`` branch which may lead to conflicts, this is a result of merging incoming
PRs that may cause upstream `HEAD` to change over time which can cause merge conflicts.
This may be confusing at first, but don't worry we are here to help. For more details
about merge conflicts click `here <https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-merge-conflicts>`_.

Syncing your feature branch with `devel` is out of scope for this documentation,
however you can use the steps below as a *guide* when you run into this issue.

You may want to take the steps to first sync devel branch and then
selectively rebase or merge ``devel`` into your feature branch.

First go to ``devel`` branch and fetch changes from upstream::

    git checkout devel
    git fetch upstream devel

Note you shouldn't be making any changes to your local ``devel`` branch, if
``git fetch`` was successful you can merge your ``devel`` with upstream as follows::

    git merge upstream/devel

Next, navigate to your feature branch and sync feature changes with devel::

    git checkout <feature-branch>
    git merge devel

.. Note:: Running above command will sync your feature branch with ``devel`` but you may have some file conflicts depending on files changed during PR. You will need to resolve them manually before pushing your changes

Instead of merge from ``devel`` you can rebase your commits interactively when syncing with ``devel``. This can be done by running::

    git rebase -i devel

Once you have synced your branch push your changes and check if file conflicts are resolved in your Pull Request::

    git push origin <feature-branch>

General Tips
-------------

1. It's good practice to link PR to an issue during commit message. Such as
stating ``Fix #132`` for fixing issue 132.

2. If you have an issue, ask your question in slack before reporting issue. If
your issue is not resolved check any open issues for resolution before creating
a new issue.

3. For new features or significant code refactor please notify maintainers and
open an issue before working on task to keep everyone informed.

4. If you open an issue, please respond back during discussion, if there is no
activity the issue will be closed.

5. Please refrain from opening duplicate issue, check if there is an existing
issue addressing similar problem, instead you can participate in discussion in
the issue or contact appropriate individuals directly in slack.

6. There should not be any branches other than ``master`` or ``devel``. Feature
branches should be pushed to your fork and not to origin.

.. _black_hook:

Configuring Black Pre-Commit Hook
-----------------------------------

To configure pre-commit hook, make sure you install `pre-commit <https://pre-commit.com/>`_ via
``pip install pre-commit``. The `pre-commit` utility should be available if you install
extra dependencies from buildtest (``pip install -r docs/requirements.txt``).

You can configure ``.pre-commit-config.yaml`` with the version of python you are using.
It is currently setup to run for python 3.7 version as follows::

    language_version: python3.7

Alter this value based on python version you are using or refer to `black version control integration <https://black.readthedocs.io/en/stable/integrations/source_version_control.html>`_.

To install the pre-commit hook run:

.. code-block:: console

    $ pre-commit install
    pre-commit installed at .git/hooks/pre-commit


This will invoke hook ``.git/hooks/pre-commit`` prior to ``git commit``. Shown below
we attempt to commit which resulted in pre commit hook and caused black to format code.

.. code-block:: console

    $ git commit -m "test black commit with precommit"
    black....................................................................Failed
    - hook id: black
    - files were modified by this hook

    reformatted buildtest/config.py
    All done! ✨ 🍰 ✨
    1 file reformatted.


If you are interested in running black locally to see diff result from black without auto-formatting code,
you can do the following:

.. code-block:: console

    $ black --check --diff .
    --- tests/test_inspect.py       2020-02-25 18:58:58.360360 +0000
    +++ tests/test_inspect.py       2020-02-25 18:59:07.336414 +0000
    @@ -18,11 +18,11 @@
     def test_distro_short():
         assert "rhel" == distro_short("Red Hat Enterprise Linux Server")
         assert "centos" == distro_short("CentOS")
         assert "suse" == distro_short("SUSE Linux Enterprise Server")
    -    x=0+1*3
    +    x = 0 + 1 * 3

The changes will be shown with lines removed or added via ``-`` and ``+``. For more details refer to `black documentation <https://github.com/psf/black>`_.

.. _isort:

isort
------

`isort <https://pycqa.github.io/isort>`__ is a python utility that will sort python imports alphabetically. We use isort as part of the CI checks, there
is a `.isort.cfg <https://github.com/buildtesters/buildtest/blob/devel/.isort.cfg>`_ that defines the isort configuration that is compatible with
`black <https://black.readthedocs.io/en/stable/>`_ utility. We have setup a pre-commit hook that can be used to automatically
run isort as part of your ``git commit`` process. This is defined in pre-commit configuration file `.pre-commit-config.yaml <https://github.com/buildtesters/buildtest/blob/devel/.pre-commit-config.yaml>`_
that can be installed by running ``pre-commit install``. Once this is setup, you will see **isort** and **black** checks are run during the commit
process.


.. code-block:: console

    $ git commit
    isort....................................................................Passed
    black....................................................................Passed
    [sphinx_fix 85d9d42c] fix issue with rendering bullet points in sphinx. This is solved by downgrading docutils to version 0.16.
     2 files changed, 5 insertions(+)

If you want to run isort, you can use the `-c` and `--diff` option to check and see diff between files. For instance in example
below we see isort reports changes to ``import`` statement

.. code-block:: shell

    $ isort -c --diff profile black  buildtest/main.py
    ERROR: /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/main.py Imports are incorrectly sorted and/or formatted.
    --- /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/main.py:before	2021-07-13 16:53:42.722718
    +++ /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/main.py:after	2021-07-13 16:54:12.135986
    @@ -1,8 +1,7 @@
     """Entry point for buildtest"""

    +import os
     import webbrowser
    -import os
    -

     from buildtest.cli import get_parser
     from buildtest.cli.build import BuildTest
    Broken 2 paths

If you want to apply the changes you can get rid of ``-c`` and ``--diff`` option and isort will apply the changes. Please
see https://pycqa.github.io/isort/docs/configuration/black_compatibility.html and https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html#isort
for documentation regarding black and isort compatibility.

.. _using_pyflakes:

pyflakes
----------

`pyflakes <https://pypi.org/project/pyflakes/>`_ is a program that checks for python source
code for errors such as unused imports. We have configured an automated check to test your incoming PR using pyflakes.
pyflakes should be available in your python environment if you installed buildtest extra
dependencies in requirements.txt (``pip install -r docs/requirements.txt``).

You can run pyflakes against any file or directory the ones of importance is running pyflakes against
buildtest source code and regression test. You can do that by running::

    pyflakes buildtest tests

Running stylechecks via ``buildtest stylecheck``
---------------------------------------------------

The ``buildtest stylecheck`` command can run the stylechecks such as `black`, `isort`, `pyflakes` which can
should be used before you commit your changes. Shown below are the available options for ``buildtest stylecheck``

.. command-output:: buildtest stylecheck --help

.. Note:: ``buildtest style`` is an alias for **buildtest stylecheck**

By default, all the checks are run when no options are specified however if you want to disable a particular style
check you can specify on command line such as ``--no-black`` will disable black style check.

Shown below is an example output of what style check will report. By default, black and isort will report changes that
will need to be fixed, if you want to apply those changes to buildtest codebase you can pass the ``--apply`` option.

.. command-output:: buildtest stylecheck

