GitHub Integrations
====================

buildtest has several github integration, including automated CI checks during PR that maintainers will check
during the code review. You should check results from the `github actions <https://github.com/buildtesters/buildtest/actions>`_
that are also typically linked as part of the pull request ci checks. You should make sure code is
formatted via black as we have automated checks for python formatting. If you have not
setup the black hook check out :ref:`black_hook`

Coverage
---------

We use `coverage <https://coverage.readthedocs.io/en/latest/>`_ to measure code
coverage of buildtest when running regression test. We use CodeCov to display
coverage reports through web interface. The coverage configuration
is managed by `.coveragerc <https://github.com/buildtesters/buildtest/blob/devel/.coveragerc>`_ file
found in the root of the repo.

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

GitHub Bots
-----------

buildtest has a few bots to do various operations that are described below.

- `Stale <https://github.com/marketplace/stale>`_  - stale bot is used to close outdated issues. This is configured in ``.github/stale.yml``. If there is no activity on a issue after certain time period, **probot-stale** will mark the issue and project maintainers can close it manually. For more details on Stale refer to the `documentation <https://probot.github.io/>`_

- `CodeCov <https://github.com/marketplace/codecov>`_ - The codecov bot will report codecov report from the issued pull request once coverage report is complete. The configuration for codecov is defined in ``.codecov.yml`` found in root of repo.

- `Pull Request Size <https://github.com/marketplace/pull-request-size>`_ - is a bot that labels Pull Request by number of **changed** lines of code.

- `Trafico <https://github.com/marketplace/trafico-pull-request-labeler>`_ - is a bot that automatically labels Pull Request depending on their status, during code reviews. The configuration is found in ``.github/trafico.yml``.
