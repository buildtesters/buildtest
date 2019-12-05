Contribution is not easy, so we created this document to describe how to get you setup
so you can contribute back and make everyone's life easier.

Preparation
=============

If you don't have a GitHub account please `register <http://github.com/join>`_ your account

Fork the repo
--------------

First, you'll need to fork the repo https://github.com/HPC-buildtest/buildtest-framework

You might need to setup your SSH keys in your git profile if you are using ssh option for cloning. For more details on
setting up SSH keys in your profile, follow instruction found in
https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to repository without requesting for password for every commit. Once you have forked the repo, clone your local repo::

  git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest-framework.git


Adding Upstream Remote
-----------------------

First you need to add the ``upstream`` repo, to do this you can issue the
following::

 git remote add upstream git@github.com/HPC-buildtest/buildtest-framework.git

The ``upstream`` tag is used to sync changes from upstream repo to keep your
repo in sync before you contribute back.

Make sure you have set your user name and email set properly in git configuration. We don't want commits from
unknown users. This can be done by setting the following::

   git config user.name "First Last"
   git config user.email "abc@example.com"

For more details see `First Time Git Setup <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>`_

Sync your branch from upstream
-------------------------------

The ``devel`` from upstream will get Pull Requests from other contributors, in-order
to sync your forked repo with upstream, run the commands below::

 cd buildtest-framework
 git checkout devel
 git fetch upstream devel
 git pull upstream devel


Once the changes are pulled locally you can sync devel branch with your
fork as follows::

 git checkout devel
 git push origin devel


Repeat this same operation with ``master`` branch if you want to sync it with
upstream repo



Feature Branch
------------------

Please make sure to create a new branch when adding and new feature. Do not
push to ``master`` or ``devel`` branch on your fork or upstream.

Create a new branch from ``devel`` as follows::

  cd buildtest-framework
  git checkout devel
  git checkout -b featureX


Once you are ready to push to your fork repo do the following::

  git push origin featureX


Once the branch is created in your fork, you can create a PR for the ``devel``
branch for ``upstream`` repo (https://github.com/HPC-buildtest/buildtest-framework)

Review
-------

Someone from the **buildtest team** will review the PR and get back to you with the feedback. If the reviewer requests
some changes, then the user is requested to make changes and update the branch used for sending PR


Documentation
----------------

buildtest documentation (https://buildtest.readthedocs.io/en/latest) is hosted by ReadTheDocs (https://readthedocs.org)
which is a documentation platform for building and hosting your docs. buildtest project can be found at
https://readthedocs.org/projects/buildtest/ which will show the recent builds and project setting. If you are interested
in being a documentation maintainer, please contact **Shahzeb Siddiqui** (``shahzebmsiddiqui@gmail.com``) to enable
access to this project. buildtest documentation is using sphinx (http://www.sphinx-doc.org/en/master/) to build the
underlying documentation.

buildtest documentation is hosted in ``docs`` found at the root of this repository. If you want to
build the documentation you will need to make sure your python environment has all the packages defined by
``requirements.txt``.

To install your python packages, you can run the following::

  pip install -r requirements.txt

To build your documentation simply run the following::

  cd docs
  make clean
  make html

It is best practice to run ``make clean`` to ensure sphinx will remove old html content from previous builds, but it is ok to
skip ``make clean`` if you are making minor changes.

Running ``make html`` will build the sphinx project and generate all the html files in ``docs/_build/html``. Once this process is
complete you may want to view the documentation. If you have ``firefox`` in your system you can simply run the following

::

  make view

This will open a ``firefox`` session to the root of your documentation that was recently generated. You will want to
make sure you have X11 forwarding in order for firefox to work properly. Refer to the ``Makefile`` to see all of the
make tags and you may run ``make`` or ``make help`` for additional help

Building API Docs
------------------

In order to build the API library for buildtest use the following command::

  make apidocs

This will run the target ``apidocs`` which is running a ``sphinx-apidocs`` command. The target location for api docs
is in ``docs/api`` so you may want to remove all the apidocs before regenerate them to ensure you have the right
contents uploaded for the push. This can be done by running the following::

  git rm -rf api/*

Next, build the api docs::

  make apidocs

Then add, commit and push content::

  git add api/*
  git commit -m <MESSAGE>
  git push

Automate Documentation Examples
--------------------------------

buildtest has a script in ``$BUILDTEST_ROOT/src/buildtest/docgen/main.py`` to automate documentation examples. This
script can be run as follows::

  cd $BUILDTEST_ROOT
  python $BUILDTEST_ROOT/src/buildtest/docgen/main.py

This assumes your buildtest environment is setup, the script will write documentation test examples in ``docs/docgen``.
Consider running this script when **adding**, **modifying**, or **removing** documentation examples. Once the test are
complete, you will want to add the tests, commit and push as follows::

  git add docs/docgen
  git commit -m <MESSAGE>
  git push

Buildtest Regression Test
--------------------------

buildtest has a suite of regression tests to verify the state of buildtest. These tests are located in
``$BUILDTEST_ROOT/tests`` and the tests can be executed using ``pytest``.

To run all the tests you can run the following::

  pytest tests/

To print passed test with output consider running with option::

  pytest -rP tests/

If you are interested in failed tests run with option::

  pytest -rf tests/

Refer to pytest `documentation <https://docs.pytest.org/en/latest/contents.html>`_  for complete list of options.

GitHub Apps
------------

The following apps are configured with buildtest.

- **CodeCov** - Codecov provides highly integrated tools to group, merge, archive and compare coverage reports

  - Link: https://codecov.io/gh/HPC-buildtest/buildtest-framework
- **GuardRails** - GuardRails provides continuous security feedback for modern development teams

  - Link: https://dashboard.guardrails.io/default/gh/HPC-buildtest

- **Travis CI** - Test and deploy with confidence. Trusted by over 800,000 users, Travis CI is the leading hosted continuous integration system.

  - Link: https://travis-ci.com/HPC-buildtest/buildtest-framework

- **Snyk** - Snyk tracks vulnerabilities in over 800,000 open source packages, and helps protect over 25,000 applications.

  - Link: https://app.snyk.io/org/hpc-buildtest/

When contributing back to buildtest, please consider checking the following GitHub apps, most important being **Travis-CI**
as it will test your pull request before merging to ``devel`` branch.

- **Stale**  - buildtest is using this app to close outdated issues. This is configured in ``.github/stale.yml``. If there is no activity on a issue after certain time period, **probot-stale** will mark the issue and project maintainers can close it manually. For more details on Stale refer to the `documentation <https://probot.github.io/>`_

- **Issue-Label-Bot** - buildtest is using this app to mark issues using Machine Learning. This app can be found in marketplace at https://github.com/marketplace/issue-label-bot. The configuration ``.github/issue_label_bot.yaml`` defines the settings for **issue-label bot** when marking new issues with the corresponding labels. For a list of predictions on all issues check the following link: https://mlbot.net/data/HPC-buildtest/buildtest-framework

Release Process
---------------

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

Formatting Code
----------------

buildtest is using `black  <https://github.com/psf/black>`_ to format Python code. We let **black** take care of
formatting the entire project so you can focus more time in development. buildtest has a GitHub action trigger in
``.github/workflows/black.yml`` that formats code upon **push** and **pull request**.

You can see the status of all GitHub actions at https://github.com/HPC-buildtest/buildtest-framework/actions




