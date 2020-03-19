GitHub Integrations
====================

buildtest has several github integration, including automated checks during PR that maintainers will check
during the PR review. You should check results from the `buildtest actions <https://github.com/HPC-buildtest/buildtest-framework/actions>`_
that are also typically linked as part of the pull request testing suite.

It's good practice to check Travis `builds <https://travis-ci.com/HPC-buildtest/buildtest-framework>`_ since we use Travis
to run regression test and Codecov and Coveralls depend on Travis to pass all checks.

You will want to make sure code is formatted via black as we have automated checks for python formatting. If you have not
setup the black hook check out :ref:`black_hook`

If you notice the black linter step in `GitHub Actions <https://github.com/HPC-buildtest/buildtest-framework/actions>`_ is
failing, make sure you have the right version of black installation.

GitHub Apps
------------

The following apps are configured with buildtest.

- `Travis CI <https://travis-ci.com/HPC-buildtest/buildtest-framework>`_ - Test and deploy with confidence. Trusted by over 800,000 users, Travis CI is the leading hosted continuous integration system.

- `CodeCov <https://codecov.io/gh/HPC-buildtest/buildtest-framework>`_ - Codecov provides highly integrated tools to group, merge, archive and compare coverage reports

- `Coveralls <https://coveralls.io/github/HPC-buildtest/buildtest-framework>`_ - Coveralls is a web service to help you track your code coverage over time, and ensure that all your new code is fully covered.

- `CodeFactor <https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework>`_ - CodeFactor instantly performs Code Review with every GitHub Commit or PR. Zero setup time. Get actionable feedback within seconds. Customize rules, get refactoring tips and ignore irrelevant issues.

- `GuardRails <https://dashboard.guardrails.io/default/gh/HPC-buildtest>`_ - GuardRails provides continuous security feedback for modern development teams

- `Snyk <https://app.snyk.io/org/hpc-buildtest/>`_  - Snyk tracks vulnerabilities in over 800,000 open source packages, and helps protect over 25,000 applications.

GitHub Actions
--------------

buildtest runs a few automated checks via GitHub Actions that can be found in ``.github/workflows``

- **Black** - buildtest is using `black  <https://github.com/psf/black>`_ to format Python code. We let **black** take care of formatting the entire project so you can focus more time in development. The workflow is defined in `black.yml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/workflows/black.yml>`_

- **URLs-checker** - buildtest is a GitHub action called **URLs-checker** found at https://github.com/marketplace/actions/urls-checker. The workflow is defined in `urlchecker.yml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/workflows/urlchecker.yml>`_

.. _black_hook:

Configuring Black Pre-Commit Hook
-----------------------------------

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

The changes will be shown with lines removed or added via ``-`` and ``+``. For more details refer to `black documentation <https://github.com/psf/black>`_.

GitHub Bots
-----------

buildtest has a few bots to do various operations that are described below.

- **Stale**  - buildtest is using `Stale <https://github.com/marketplace/stale>`_ to close outdated issues. This is configured in ``.github/stale.yml``. If there is no activity on a issue after certain time period, **probot-stale** will mark the issue and project maintainers can close it manually. For more details on Stale refer to the `documentation <https://probot.github.io/>`_

- **Issue-Label-Bot** - buildtest is using `Issue-Label-Bot <https://github.com/marketplace/issue-label-bot>`_ to mark issues using Machine Learning. The configuration can be found at `issue_label_bot.yaml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/issue_label_bot.yaml>`_. The **issue-label bot** will marking incoming issues with the corresponding labels. For a list of predictions on all issues check the following link: https://mlbot.net/data/HPC-buildtest/buildtest-framework
