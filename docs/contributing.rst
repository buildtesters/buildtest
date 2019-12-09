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

Contributing Topics
--------------------

.. toctree::

   contributing/setup.rst
   contributing/build_documentation.rst
   contributing/regression_testing.rst
   contributing/release_process.rst