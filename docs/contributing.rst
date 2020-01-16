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

- **Coverall**: https://coveralls.io/github/HPC-buildtest/buildtest-framework

- **CodeFactor**: https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework

- **Snyk**: https://app.snyk.io/org/hpc-buildtest/

- **GuardRails**: https://dashboard.guardrails.io/default/gh/HPC-buildtest


When contributing back to buildtest, please consider checking the following GitHub apps, most important being **Travis-CI**
as it will test your pull request before merging to ``devel`` branch.

GitHub Actions
-----------------

buildtest runs a few automated checks via GitHub Actions that can be found in ``.github/workflows``

- **Black** - buildtest is using `black  <https://github.com/psf/black>`_ to format Python code. We let **black** take care of formatting the entire project so you can focus more time in development. The workflow is defined in `black.yml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/workflows/black.yml>`_

- **URLs-checker** - buildtest is a GitHub action called **URLs-checker** found at https://github.com/marketplace/actions/urls-checker. The workflow is defined in `urlchecker.yml <https://github.com/HPC-buildtest/buildtest-framework/blob/devel/.github/workflows/urlchecker.yml>`_

GitHub Bots
-------------

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