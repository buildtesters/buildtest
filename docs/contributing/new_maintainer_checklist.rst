New Maintainers Checklist
===========================

Onboarding Email
------------------

This guide is to help onboard new maintainers into the buildtest project. To get
started send an invitation email as follows::

    We are pleased to invite you to the buildtest project and become a
    buildtesters (a.k.a buildtest maintainer). We understand your time is
    valuable; therefore we request a minimal effort of 2-3hrs per week towards buildtest.

    As a buildtesters, you will be working on the following:

      * Monitor and triage issues
      * Assist user in slack channel (#general)
      * Update documentation
      * Review or triage Pull Request
      * Issue new pull request
      * Troubleshoot build errors in regression test or CI checks

    As a buildtesters you may be granted elevated privilege to the following
    services: GitHub, ReadTheDocs, Slack, and Google Analytics. As a
    buildtesters, you agree to be accessible on Slack as our primary communication
    channel.

    If you agree to these terms, you will be assigned to work with another buildtest
    maintainer in your first two weeks. Once you are confident in your duties, we
    will let you work independently at your own pace, should you need help please
    contact one of the buildtesters.

    Please review the contributing guide: https://buildtest.readthedocs.io/en/devel/contributing.html
    if you are unsure about your responsibilities as a buildtesters.

    If you agree to these terms and conditions, please reply "I CONFIRM".

    Thanks,
    buildtest

Onboarding Checklist
---------------------

 - Please make sure the maintainer has a GitHub account if not please create an account at https://github.com/join.

 - Ensure user has setup `two-factor authentication (2FA) <https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/securing-your-account-with-two-factor-authentication-2fa>`_ with GitHub.

 - Invite member to `buildtesters organization <https://github.com/orgs/buildtesters/people>`_.

 - Add member to `buildtest repository <https://github.com/buildtesters/buildtest/settings/access>`_ with **Role: Maintain**.

 - Invite member to `Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_ and preferably install Slack on your workstation and phone. Please follow instructions to download slack for `Windows <https://slack.com/downloads/windows>`_, `Mac <https://slack.com/downloads/mac>`_,  or `Android <https://slack.com/downloads/android>`_. Slack is available on Apple Store and Google Play Store.

 - Once member is added to Slack, ensure member has the appropriate account type. Generally you will want member to be a **Workspace Admin** for more details see `Slack Roles & Permissions <https://slack.com/help/categories/360000049043-Getting-started#understand-roles-permissions>`_.

 - Ensure member has an account at ReadTheDocs if not please request member to create an account at https://readthedocs.org/accounts/signup/. Once member has an account please add member to buildtest readthedocs project at https://readthedocs.org/dashboard/buildtest/users/. This will ensure user has ability to access readthedocs platform when troubleshooting build errors related to documentation.


New Member Reference Material
-------------------------------

buildtest codebase is written in Python 3, if you are new to Python you will want to
check out the python 3 tutorial: https://docs.python.org/3/tutorial/. This is a good
starting point to understand python basics. If you are familiar with Python 2 you may want to review
the `Python 2-3 cheat sheet <http://python-future.org/compatible_idioms.html>`_.

buildtest relies on `YAML <https://yaml.org/>`_ and `JSON Schema <https://json-schema.org/>`_,
you should review `Understanding JSON Schema <https://json-schema.org/understanding-json-schema/>`_ article
as it provides a thorough overview of JSON Schema. There are several resources
to help you learn YAML for instance you can check out:

- https://www.tutorialspoint.com/yaml/index.htm
- https://learnxinyminutes.com/docs/yaml/

buildtest has a regression test that is run via `pytest <https://docs.pytest.org/en/stable/>`_. You
should be familiar with pytest and it's usage and documentation as it will help you write
regression test. The regression test makes use of `coverage <https://coverage.readthedocs.io/>`_
to measure code coverage of buildtest source code. This is configured using `.coveragerc` file located
in top of repo. The coverage data to `codecov <https://codecov.io/gh/buildtesters/buildtest/>`_


buildtest has several CI checks written in GitHub workflows. These are found in ``.github/workflows``
directory of buildtest. You should familiarize yourself with `Worflow Syntax <https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions>`_.

Git is essential to contributing back to buildtest, often times you will need to
make changes and push them to your fork via git. In order to use git you can check
out these links:

- https://guides.github.com/introduction/git-handbook/
- https://git-scm.com/docs/gittutorial
- https://guides.github.com/
- https://lab.github.com/

buildtest documentation is built on `sphinx <https://www.sphinx-doc.org/en/master/>`_
and hosted via `readthedocs <https://readthedocs.org/>`_. Be sure to check out
`documentation on readthedocs  <https://docs.readthedocs.io/en/stable/>`_ to understand
how it works. The buildtest project is hosted at https://readthedocs.org/projects/buildtest/ which
hosts the public documentation at https://buildtest.readthedocs.io/. The documentation
pages are written in `reStructured Text (rST) <https://docutils.sourceforge.io/rst.html>`_
which is Sphinx's markup language when hosting the docs.