GitHub Integrations
====================

buildtest has several CI checks that are run when you create a Pull Request, it is your responsibility to review
the CI checks and make sure all checks are passing. Each pull request will show the CI checks, you can see the
`github actions <https://github.com/buildtesters/buildtest/actions>`_ that are also typically linked as part of the
pull request.

Coverage
---------

We use `coverage <https://coverage.readthedocs.io/en/latest/>`_ to measure code
coverage of buildtest when running regression test. We use CodeCov to display
coverage reports through web interface. The coverage configuration
is managed by `pyproject.toml <https://github.com/buildtesters/buildtest/blob/devel/pyproject.toml>`_ file
found in the root of the repo.

Whenever you add new feature to buildtest, please add regression test with test
coverage to help maintainers review new feature request. For more details on running
coverage tests see :ref:`coverage_test`.

CodeCov
-------

`Codecov <https://docs.codecov.io/docs>`__  report coverage details in web-browser.
CodeCov can perform `pull request comments <https://docs.codecov.io/docs/pull-request-comments>`_
after coverage report is uploaded to Codecov which is useful for reviewer and assignee
to see status of coverage report during PR review process. The codecov file
`.codecov.yml <https://github.com/buildtesters/buildtest/blob/devel/.codecov.yml>`_
is used for configuration codecov. For more details on codecov yaml file see https://docs.codecov.io/docs/codecov-yaml.

GitHub Bots
-----------

buildtest has a few bots to do various operations that are described below.

- `Stale <https://github.com/marketplace/actions/close-stale-issues>`_  - stale bot is used to close outdated issues. This is configured in ``.github/stale.yml``. If there is no activity on a issue after certain time period, **probot-stale** will mark the issue and project maintainers can close it manually. For more details on Stale refer to the `documentation <https://probot.github.io/>`_

- `CodeCov <https://github.com/marketplace/codecov>`__ - The codecov bot will report codecov report from the issued pull request once coverage report is complete. The configuration for codecov is defined in ``.codecov.yml`` found in root of repo.

- `Pull Request Size <https://github.com/marketplace/pull-request-size>`_ - is a bot that labels Pull Request by number of **changed** lines of code.