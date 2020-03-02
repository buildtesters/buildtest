Contributing Guide
==================

This document explains how you can contribute back to buildtest.

There are many ways you can help contribute to buildtest that may include

- File an `issue <https://github.com/HPC-buildtest/buildtest-framework/issues>`_ with the framework
- Proofread documentation and report or fix issues
- Participate in discussions and join the slack `channel <http://hpcbuildtest.slack.com>`_
- Share your tests
- Provide feedback on buildtest options.

    1. What features you *like*/*dislike*
    2. What features you would like to have
    3. What testing capabilities matter most for you

Reporting an Issue
-------------------

Please report all issues regarding the framework at https://github.com/HPC-buildtest/buildtest-framework/issues

GitHub Apps
------------

The following apps are configured with buildtest.

- **Travis CI** - Test and deploy with confidence. Trusted by over 800,000 users, Travis CI is the leading hosted continuous integration system.

- **CodeCov** - Codecov provides highly integrated tools to group, merge, archive and compare coverage reports

- **Coverall** - Coveralls is a web service to help you track your code coverage over time, and ensure that all your new code is fully covered.

- **CodeFactor** - CodeFactor instantly performs Code Review with every GitHub Commit or PR. Zero setup time. Get actionable feedback within seconds. Customize rules, get refactoring tips and ignore irrelevant issues.

- **GuardRails** - GuardRails provides continuous security feedback for modern development teams

- **Snyk** - Snyk tracks vulnerabilities in over 800,000 open source packages, and helps protect over 25,000 applications.

Links to the following apps

- **Travis**: https://travis-ci.com/HPC-buildtest/buildtest-framework

- **CodeCov**: https://codecov.io/gh/HPC-buildtest/buildtest-framework

- **Coveralls**: https://coveralls.io/github/HPC-buildtest/buildtest-framework

- **CodeFactor**: https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework

- **Snyk**: https://app.snyk.io/org/hpc-buildtest/

- **GuardRails**: https://dashboard.guardrails.io/default/gh/HPC-buildtest


When contributing back to buildtest, please consider checking the following GitHub apps, most important being **Travis-CI**
as it will test your pull request before merging to ``devel`` branch.



GitHub Actions
--------------

buildtest runs a few automated checks via GitHub Actions that can be found in ``.github/workflows``

- **Black** - buildtest is using `black  <https://github.com/psf/black>`_ to format Python code. We let **black** take care of formatting the entire project so you can focus more time in development. The workflow is defined in `black.yml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/workflows/black.yml>`_

- **URLs-checker** - buildtest is a GitHub action called **URLs-checker** found at https://github.com/marketplace/actions/urls-checker. The workflow is defined in `urlchecker.yml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/workflows/urlchecker.yml>`_

GitHub Hooks
------------

The above actions check formatting, but are conservative and do not do commits to fix issues on behalf of the user.
To support an easier workflow, we have provided a git hook that you can install locally to run black directly before each
commit. To install the hook, simply copy the file to the ``.git/hooks`` folder as follows::

    cp .github/hooks/pre-commit .git/hooks/


This hook will exit on error either if you don't have black installed::

    pip install black==19.3b0


or if you have black installed, but running it on the repository code results in an error due
to a functional issue with the code. Code that simply needs to be formatted will be formatted,
and then the commit will follow.

Once you have installed the ``pre-commit`` hook and black, then you can expect
black will auto-format your code during the commit phase. Here is a snapshot of
what the pre-commit hook will do ::

    $ git commit -m "test black on one of the regtest"
    Black is installed
    reformatted /mxg-hpc/users/ssi29/buildtest-framework/tests/test_inspect.py
    All done! ✨ 🍰 ✨
    1 file reformatted, 39 files left unchanged.
    [test_black_hook 008fc62] test black on one of the regtest
     1 file changed, 1 insertion(+)

The pre-commit hook will auto-format specific directories where python files are found. Refer to the
pre-commit hook (``.github/hooks/pre-commit``) for more details.

If you are interested in running black locally to see diff result from black without auto-formatting code,
you can do the following::

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

The changes will be shown with lines removed or added via ``-`` and ``+``. For more details refer to black
`documentation <https://github.com/psf/black>`_.

GitHub Bots
-----------

Buildtest has a few bots to do various operations that are described below.

- **Stale**  - buildtest is using `Stale <https://github.com/marketplace/stale>`_ to close outdated issues. This is configured in ``.github/stale.yml``. If there is no activity on a issue after certain time period, **probot-stale** will mark the issue and project maintainers can close it manually. For more details on Stale refer to the `documentation <https://probot.github.io/>`_

- **Issue-Label-Bot** - buildtest is using `Issue-Label-Bot <https://github.com/marketplace/issue-label-bot>`_ to mark issues using Machine Learning. The configuration can be found at `issue_label_bot.yaml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/issue_label_bot.yaml>`_. The **issue-label bot** will marking incoming issues with the corresponding labels. For a list of predictions on all issues check the following link: https://mlbot.net/data/HPC-buildtest/buildtest-framework

Contributing Topics
--------------------

.. toctree::

   contributing/setup.rst
   contributing/build_documentation.rst
   contributing/regression_testing.rst
   contributing/release_process.rst
