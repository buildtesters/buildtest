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
    maintainer in your first two weeks. Once you are confident in your duties, you
    will work independently at your own pace, should you need assistance please
    contact one of the maintainers.

    Please review the contributing guide: https://buildtest.readthedocs.io/en/devel/contributing.html
    if you are unsure about your responsibilities as a maintainer.

    If you agree to these terms and conditions, please reply "I CONFIRM".

    Thanks,
    buildtest

Onboarding Checklist
---------------------

The on-boarding checklist is used to transition an existing contributor to maintainer roler. A maintainer should exercise
judgement, when on-boarding a contributor to maintainer role which has elevated priviledge to buildtest operations.

 - Please make sure the maintainer has a GitHub account if not please create an account at https://github.com/join.

 - Ensure user has setup `two-factor authentication (2FA) <https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/securing-your-account-with-two-factor-authentication-2fa>`_ with GitHub.

 - Invite member to `buildtesters organization <https://github.com/orgs/buildtesters/people>`_.

 - Add member to `buildtest repository <https://github.com/buildtesters/buildtest/settings/access>`_ with **Role: Maintain**.

 - Invite member to join `slack channel <https://communityinviter.com/apps/hpcbuildtest/buildtest-slack-invitation>`_ and preferably install Slack on your workstation and phone. Please follow instructions to download slack for `Windows <https://slack.com/downloads/windows>`_, `Mac <https://slack.com/downloads/mac>`_,  or `Android <https://slack.com/downloads/android>`_. Slack is available on Apple Store and Google Play Store.

 - Once member is added to Slack, ensure member has the appropriate account type. Generally you will want member to be a **Workspace Admin** for more details see `Slack Roles & Permissions <https://slack.com/help/categories/360000049043-Getting-started#understand-roles-permissions>`_.

 - Ensure member has an account at ReadTheDocs if not please request member to create an account at https://readthedocs.org/accounts/signup/. Once member has an account please add member to buildtest readthedocs project at https://readthedocs.org/dashboard/buildtest/users/. This will ensure user has ability to access readthedocs platform when troubleshooting build errors related to documentation.

  - Please grant user access to NERSC System, if he/she does not have an account, please have them fill out a form and apply for project **m3503**. For more detail see https://docs.nersc.gov/accounts/.

  - We have a buildtest mirror at https://software.nersc.gov/NERSC/buildtest, you should consider giving maintainer elevated privilege such as `Maintainer` role. Please go to https://software.nersc.gov/NERSC/buildtest/-/project_members and add member to group with the desired role. Note `maintainer` access is only required to see project settings, for more operations one can get by with `developer` permission which allows one to see CI job results.

  - We have a mirror of buildtest at `Oak Ridge Leadership Computing Facility (OLCF) <https://docs.olcf.ornl.gov/>`_ system. Please have the individual apply for **new** OLCF account, for more details see https://docs.olcf.ornl.gov/accounts/index.html. You should contact `Shahzeb Siddiqui <mailto:shahzebsiddiqui@lbl.gov>`_ in-order for you to be added to OLCF project account. Once you have an account, please make sure you have access to project https://code.ornl.gov/ecpcitest/buildtest which is the mirror of buildtest. Please make sure the individual has `maintainer` role.

Offboarding Checklist
----------------------

The offboarding checklist is meant to remove privileges for maintainers that decide to leave the project or
transition to new role where certain permissions are no longer needed. First confirm with individual that
he/she would like to be removed as maintainer. Often times, the individual may continue contribution to
buildtest but doesn't need elevated privilege.

To get started please consider the following when off-boarding maintainers

- Check buildtesters organization https://github.com/orgs/buildtesters/people and update the membership for the individual

- Check buildtest settings https://github.com/buildtesters/buildtest/settings/access to determine appropriate role for member. If individual has a `maintainer` role, please update this to a lower permission scope.

- Remove `maintainers` role from buildtest project in ReadTheDocs https://readthedocs.org/dashboard/buildtest/users/

- Please reassign any `open issues <https://github.com/buildtesters/buildtest/issues>`_ for the maintainer, unless he/she decides to work on the task.

- Follow up with any open `Pull Requests <https://github.com/buildtesters/buildtest/pulls>`_, if you can get maintainer to finish task that would be great, otherwise please reassign pull request to another maintainer or close task.

- Check if maintainer has access to Google Analytics for buildtest documentation, if so, please remove user email from Google Analytics.