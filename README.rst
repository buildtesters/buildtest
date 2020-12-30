| |license| |docs| |codecov| |slack| |codefactor| |gh_pages_master| |gh_pages_devel| |checkurls| |dailyurlcheck| |blackformat| |clichecks| |regressiontest| |buildtest_scripts| |core_infrastructure| |black|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
    :target: http://hpcbuildtest.slack.com

.. |license| image:: https://img.shields.io/github/license/buildtesters/buildtest.svg

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

.. |clichecks| image:: https://github.com/buildtesters/buildtest/workflows/buildtest%20cli%20test/badge.svg 
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

buildtest
---------

buildtest is a HPC testing framework that helps facilities write acceptance test
more efficiently. Buildtest provides a framework for facility to write tests in `YAML <https://yaml.org/>`_
called *Buildspecs* and buildtest handles how to create testscript and run the test on your system.
Buildtest makes use of `jsonschema <https://json-schema.org/>`_
to specify schema how Buildspecs are written and validated. Once you learn buildtest,
you can start writing tests.

To get started with buildtest see `Installing buildtest <https://buildtest.readthedocs.io/en/latest/installing_buildtest.html>`_.

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

buildtest source code is under ``buildtest`` directory found in the root of this
repository. The documentation is under ``docs`` which consist of ``Makefile``
and ``conf.py`` to build the sphinx project along with documentation pages in
ReStructuredText (rst). The regression test are found in top-level directory
named ``tests`` and the test suite is run via ``pytest``.

Slack
------

Click the `Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_ to get in
touch with the buildtest community. If you already have an account then access
the Slack Channel `here  <https://hpcbuildtest.slack.com>`_.

Contributing Back
-------------------

We would love to get your contribution, if you are not sure check out the
`Contribution Guide <https://buildtest.readthedocs.io/en/latest/contributing.html>`_ to get started.

Author
-------

buildtest was founded by `Shahzeb Siddiqui <https://github.com/shahzebsiddiqui>`_.

LICENSE
--------

buildtest is released under the MIT License. See
`LICENSE <https://github.com/buildtesters/buildtest/blob/master/LICENSE>`_ for more details.
