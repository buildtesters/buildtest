| |docs| |codecov| |slack| |release| |ascent_pipeline_status| |cori_pipeline_status| |installation| |regressiontest| |buildtest_scripts|  |gh_pages_master| |gh_pages_devel| |checkurls| |dailyurlcheck| |codefactor| |blackformat|  |black| |issues| |open_pr| |commit_activity_yearly| |commit_activity_monthly| |core_infrastructure| |zenodo|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
    :target: http://hpcbuildtest.slack.com

.. |ascent_pipeline_status| image::  https://code.ornl.gov/ecpcitest/buildtest/badges/devel/pipeline.svg
   :target: https://code.ornl.gov/ecpcitest/buildtest/-/commits/devel
 
.. |cori_pipeline_status| image:: https://software.nersc.gov/siddiq90/buildtest/badges/devel/pipeline.svg
   :target: https://software.nersc.gov/siddiq90/buildtest/-/commits/devel

.. |release| image:: https://img.shields.io/github/v/release/buildtesters/buildtest.svg
   :target: https://github.com/buildtesters/buildtest/releases
   
.. |issues| image:: https://img.shields.io/github/issues/buildtesters/buildtest.svg 
    :target: https://github.com/buildtesters/buildtest/issues
    
.. |open_pr| image:: https://img.shields.io/github/issues-pr/buildtesters/buildtest.svg
    :target: https://github.com/buildtesters/buildtest/pulls
    
.. |commit_activity_yearly| image:: https://img.shields.io/github/commit-activity/y/buildtesters/buildtest.svg
 
.. |commit_activity_monthly| image:: https://img.shields.io/github/commit-activity/m/buildtesters/buildtest.svg

.. |core_infrastructure| image:: https://bestpractices.coreinfrastructure.org/projects/3469/badge

.. |codecov| image:: https://codecov.io/gh/buildtesters/buildtest/branch/devel/graph/badge.svg
    :target: https://codecov.io/gh/buildtesters/buildtest

.. |codefactor| image:: https://www.codefactor.io/repository/github/buildtesters/buildtest/badge
    :target: https://www.codefactor.io/repository/github/buildtesters/buildtest
    :alt: CodeFactor

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |checkurls| image:: https://github.com/buildtesters/buildtest/workflows/Check%20URLs/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |blackformat| image:: https://github.com/buildtesters/buildtest/workflows/Black%20Formatter/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |installation| image:: https://github.com/buildtesters/buildtest/workflows/installation/badge.svg
   :target: https://github.com/buildtesters/buildtest/actions

.. |regressiontest| image:: https://github.com/buildtesters/buildtest/workflows/regressiontest/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |buildtest_scripts| image:: https://github.com/buildtesters/buildtest/workflows/buildtest_scripts/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |gh_pages_devel| image:: https://github.com/buildtesters/buildtest/workflows/Upload%20JSON%20Schema%20to%20gh-pages%20on%20devel/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |gh_pages_master| image:: https://github.com/buildtesters/buildtest/workflows/Upload%20JSON%20Schema%20to%20gh-pages%20for%20master%20branch/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions    

.. |dailyurlcheck| image:: https://github.com/buildtesters/buildtest/workflows/Daily%20Check%20URLs/badge.svg
   :target: https://github.com/buildtesters/buildtest/actions

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3967143.svg
   :target: https://doi.org/10.5281/zenodo.3967143

buildtest
---------

buildtest is a testing framework for HPC facilities to write acceptance test
for their system. In buildtest, you will write tests in `YAML <https://yaml.org/>`_
called **Buildspecs** which is a test recipe used by buildtest for generating test scripts.
buildtest will process *buildspecs* and automatically create shell-scripts and run them
on your system via executors (local, batch). Currently, we support LSF, Slurm, and Cobalt
scheduler for job submission. We use `jsonschema <https://json-schema.org/>`_ to define structure of buildspecs.

Installation
--------------


Installing buildtest, is relatively easy. Just clone this repo and source the setup script::

    git clone https://github.com/buildtesters/buildtest.git
    cd buildtest
    source setup.sh


For more details see `installing buildtest <https://buildtest.readthedocs.io/en/latest/installing_buildtest.html>`_.


Schema Development
-------------------

The schemas are found in top-level folder `buildtest/schemas/ <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas>`_
and published via Github Pages at https://buildtesters.github.io/buildtest/. Each schema has a unique URI defined
by `$id <https://json-schema.org/understanding-json-schema/structuring.html#the-id-property>`_.

For any issues with schema, please create an `issue <https://github.com/buildtesters/buildtest/issues>`_ in buildtest.

References
------------

- Documentation: http://buildtest.rtfd.io/

- Schema Docs: https://buildtesters.github.io/buildtest/

- ReadTheDocs: https://readthedocs.org/projects/buildtest/

- CodeCov: https://codecov.io/gh/buildtesters/buildtest

- CodeFactor: https://www.codefactor.io/repository/github/buildtesters/buildtest

- Snyk: https://app.snyk.io/org/buildtesters/

Why buildtest?
---------------

Read https://buildtest.readthedocs.io/en/latest/what_is_buildtest.html to
understand why we need buildtest and what we are trying to solve.

Documentation
-------------

buildtest `documentation <http://buildtest.readthedocs.io/en/latest/>`_  is your
source for getting help with buildtest. If you get stuck check out the
`current issues <https://github.com/buildtesters/buildtest/issues>`_ to see
if you face similar issue. If all else fails please create a ticket.

Source Code
------------

buildtest source code is under `buildtest <https://github.com/buildtesters/buildtest/tree/devel/buildtest>`_
directory found in the root of this repository. The documentation pages are located in
`docs <https://github.com/buildtesters/buildtest/tree/devel/docs>`_ folder
which consist of `Makefile <https://github.com/buildtesters/buildtest/blob/devel/docs/Makefile>`_ and
`conf.py <https://github.com/buildtesters/buildtest/blob/devel/docs/conf.py>`_ to build the sphinx project along with documentation pages in
ReStructuredText (rst). The regression test are found in top-level directory
named `tests <https://github.com/buildtesters/buildtest/tree/devel/tests>`_ and the test suite is run via `pytest <https://docs.pytest.org/en/stable/>`_.

Slack
------

Slack is **preferred* method to answer your questions,  best way to ask for questions, you
Click the `Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_ to get in
touch with the buildtest community. If you already have an account then access
the Slack Channel `here  <https://hpcbuildtest.slack.com>`_.

- Self Invite: https://hpcbuildtest.herokuapp.com/
- Slack Channel: https://hpcbuildtest.slack.com

Contributing Back
-------------------

We would love to get your feedback and contribution, for more details see
`contribution guide <https://buildtest.readthedocs.io/en/latest/contributing.html>`_.

Author
-------

buildtest was founded by `Shahzeb Siddiqui <https://github.com/shahzebsiddiqui>`_.

LICENSE
--------

buildtest is released under the MIT License. See
`LICENSE <https://github.com/buildtesters/buildtest/blob/master/LICENSE>`_ for more details.
