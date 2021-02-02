GitHub Integrations
====================

buildtest has several github integration, including automated checks during PR that maintainers will check
during the PR review. You should check results from the `buildtest actions <https://github.com/buildtesters/buildtest/actions>`_
that are also typically linked as part of the pull request ci checks.

You will want to make sure code is formatted via black as we have automated checks for python formatting. If you have not
setup the black hook check out :ref:`black_hook`

If you notice the black linter step in `GitHub Actions <https://github.com/buildtesters/buildtest/actions>`_ is
failing, make sure you have the right version of black installation.

GitHub Apps
------------

The following apps are configured with buildtest.

- `CodeCov <https://codecov.io/gh/buildtesters/buildtest>`_ - Codecov provides highly integrated tools to group, merge, archive and compare coverage reports

- `CodeFactor <https://www.codefactor.io/repository/github/buildtesters/buildtest>`_ - CodeFactor instantly performs Code Review with every GitHub Commit or PR. Zero setup time. Get actionable feedback within seconds. Customize rules, get refactoring tips and ignore irrelevant issues.

- `Snyk <https://app.snyk.io/org/buildtesters/>`_  - Snyk tracks vulnerabilities in over 800,000 open source packages, and helps protect over 25,000 applications.

Coverage
---------

We use `coverage <https://coverage.readthedocs.io/en/latest/>`_ to measure code
coverage of buildtest when running regression test. We use CodeCov to display
coverage reports through web interface. The coverage configuration
is managed by *.coveragerc* file found in the root of the repo.

Whenever you add new feature to buildtest, please add regression test with test
coverage to help maintainers review new feature request. For more details on running
coverage tests see :ref:`coverage_test`.

CodeCov
-------

`Codecov <https://docs.codecov.io/docs>`_  report coverage details in web-browser.
CodeCov can perform `pull request comments <https://docs.codecov.io/docs/pull-request-comments>`_
after coverage report is uploaded to Codecov which is useful for reviewer and assignee
to see status of coverage report during PR review process. The codecov file
`.codecov.yml <https://github.com/buildtesters/buildtest/blob/devel/.codecov.yml>`_
is used for configuration codecov. For more details on codecov yaml file see https://docs.codecov.io/docs/codecov-yaml.

Gitlab CI checks
------------------

buildtest has automated CI checks on gitlab servers: https://software.nersc.gov and https://code.ornl.gov. The
gitlab pipelines are stored in `.gitlab <https://github.com/buildtesters/buildtest/tree/devel/.gitlab>`_ directory found
in root of repository.

The `mirror.yml <https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/mirror.yml>`_ github workflow
is responsible for mirroring and trigger CI check and return result back to github PR. Currently, we are using github
action `stenongithub/gitlab-mirror-and-ci-action <https://github.com/stenongithub/gitlab-mirror-and-ci-action>`_ to perform pull mirroring and triggering CI job.

The gitlab server https://software.nersc.gov is hosted at NERSC. The following steps were taken to setup pipeline

1. Create a Personal Access token with **read_api**, **read_repository**, **write_repository** scope at https://software.nersc.gov/-/profile/personal_access_tokens
2. Define a secret **CORI_GITLAB_PASSWORD** at https://github.com/buildtesters/buildtest/settings/secrets/actions with token value generated in step 1
3. Import buildtest project from github at https://software.nersc.gov/siddiq90/buildtest
4. Add variable **SECRET_CODECOV_TOKEN** in https://software.nersc.gov/siddiq90/buildtest/-/settings/ci_cd that contains codecov token found at https://app.codecov.io/gh/buildtesters/buildtest/settings
5. Change gitlab CI configuration file to `.gitlab/cori.yml <https://github.com/buildtesters/buildtest/blob/devel/.gitlab/cori.yml>`_ under **Settings > CI/CD > General pipelines**. For more details see https://docs.gitlab.com/ee/ci/pipelines/settings.html#custom-cicd-configuration-path

The gitlab server https://code.ornl.gov is hosted at OLCF which has access to systems like Summit and Ascent. We performed similar steps at as shown above with
slight modification

1. Create a Personal access token with same scope at https://code.ornl.gov/-/profile/personal_access_tokens
2. Define a secret **OLCF_GITLAB_PASSWORD** at https://github.com/buildtesters/buildtest/settings/secrets/actions
3. Import buildtest project at https://code.ornl.gov/ecpcitest/buildtest. Currently, all projects in ``ecpcitest`` project group has access to gitlab runners.
4. Add variable **SECRET_CODECOV_TOKEN** in https://code.ornl.gov/ecpcitest/buildtest/-/settings/ci_cd that contains codecov token found at https://app.codecov.io/gh/buildtesters/buildtest/settings
5. Change gitlab CI configuration file to `.gitlab/olcf.yml <https://github.com/buildtesters/buildtest/blob/devel/.gitlab/olcf.yml>`_

Currently, the gitlab pipelines are triggered manually which requires a user to have access to the gitlab project to run the pipeline. The pipelines can be run manually at
https://software.nersc.gov/siddiq90/buildtest/-/pipelines and https://code.ornl.gov/ecpcitest/buildtest/-/pipelines

The github workflow `mirror.yml <https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/mirror.yml>`_
defines gitlab configuration for each mirror. Any changes to mirror path must be addressed in this workflow to ensure pull mirroring is
done properly.

GitHub Actions
--------------

buildtest runs a few automated checks via GitHub Actions that can be found in ``.github/workflows``

- `Black  <https://github.com/psf/black>`_ - Black auto-formats Python code, so we let **black** take care of formatting the entire project so you can focus more time in development. The workflow is defined in `black.yml <https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/black.yml>`_.

- `urlchecker-action <https://github.com/urlstechie/urlchecker-action>`_ - is a GitHub action to collect and check URLs in project code and documentation. There is an automated check for every issued PR and the workflow is defined in `urlchecker.yml <https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/urlchecker.yml>`_

.. _black_hook:

Configuring Black Pre-Commit Hook
-----------------------------------

To configure pre-commit hook, make sure ``pre-commit`` is available if not
``pip install pre-commit``. The pre-commit is available if you install buildtest
dependencies.

You can configure ``.pre-commit-config.yaml`` with the version of python you are using.
It is currently setup to run for python 3.7 version as follows::

    language_version: python3.7

Alter this value based on python version you are using or refer to `black version control integration <https://black.readthedocs.io/en/stable/version_control_integration.html>`_.

To install the pre-commit hook run::

    $ pre-commit install
    pre-commit installed at .git/hooks/pre-commit


This will invoke hook ``.git/hooks/pre-commit`` prior to ``git commit``. Shown below
we attempt to commit which resulted in pre commit hook and caused black to format code.

::

    $ git commit -m "test black commit with precommit"
    black....................................................................Failed
    - hook id: black
    - files were modified by this hook

    reformatted buildtest/config.py
    All done! ✨ 🍰 ✨
    1 file reformatted.


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

.. _pyflakes:

pyflakes
----------

There is an automated test to check for unused imports using pyflakes. pyflakes
should be available in your python environment if you installed buildtest extra
dependencies in requirements.txt (``pip install -r docs/requirements.txt``).

You can run pyflakes against buildtest source by running::

    pyflakes buildtest

If you see errors, please fix them and wait for CI checks to pass.


GitHub Bots
-----------

buildtest has a few bots to do various operations that are described below.

- `Stale <https://github.com/marketplace/stale>`_  - stale bot is used to close outdated issues. This is configured in ``.github/stale.yml``. If there is no activity on a issue after certain time period, **probot-stale** will mark the issue and project maintainers can close it manually. For more details on Stale refer to the `documentation <https://probot.github.io/>`_

- `CodeCov <https://github.com/marketplace/codecov>`_ - The codecov bot will report codecov report from the issued pull request once coverage report is complete. The configuration for codecov is defined in ``.codecov.yml`` found in root of repo.

- `Pull Request Size <https://github.com/marketplace/pull-request-size>`_ - is a bot that labels Pull Request by number of **changed** lines of code.

- `Trafico <https://github.com/marketplace/trafico-pull-request-labeler>`_ - is a bot that automatically labels Pull Request depending on their status, during code reviews. The configuration is found in ``.github/trafico.yml``.
