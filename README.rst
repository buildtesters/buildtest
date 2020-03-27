| |license| |docs| |travis| |codecov| |coveralls| |slack| |codefactor| |core_infrastructure| |black| |tags| 

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
.. |license| image:: https://img.shields.io/github/license/HPC-buildtest/buildtest-framework.svg
.. |core_infrastructure| image:: https://bestpractices.coreinfrastructure.org/projects/3469/badge
.. |tags| image:: https://img.shields.io/github/v/tag/HPC-buildtest/buildtest-framework.svg
.. |codecov| image:: https://codecov.io/gh/HPC-buildtest/buildtest-framework/branch/devel/graph/badge.svg
    :target: https://codecov.io/gh/HPC-buildtest/buildtest-framework
.. |coveralls| image:: https://coveralls.io/repos/github/HPC-buildtest/buildtest-framework/badge.svg?branch=devel
    :target: https://coveralls.io/github/HPC-buildtest/buildtest-framework?branch=devel
.. |codefactor| image:: https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework/badge
   :target: https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework
   :alt: CodeFactor
.. |travis| image:: https://travis-ci.com/HPC-buildtest/buildtest-framework.svg?branch=devel
    :target: https://travis-ci.com/HPC-buildtest/buildtest-framework
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

buildtest
---------

buildtest is a software stack testing framework that automates test creation and execution to help users and 
HPC facilities to better support and validate their software stack. buildtest can provide a means to share central repositories 
with collections of tests for scientific software. buildtest makes use of `YAML <https://yaml.org/>`_ configuration to write
test configuration that is reusable and adaptable to other HPC sites.

To get started with buildtest see `Installing buildtest <https://buildtest.readthedocs.io/en/latest/installing_buildtest.html>`_

References
------------

- Documentation: http://buildtest.rtfd.io/

- ReadTheDocs: https://readthedocs.org/projects/buildtest/

- Travis: https://travis-ci.com/HPC-buildtest/buildtest-framework

- CodeCov: https://codecov.io/gh/HPC-buildtest/buildtest-framework

- Coveralls: https://coveralls.io/github/HPC-buildtest/buildtest-framework

- CodeFactor: https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework

- Snyk: https://app.snyk.io/org/hpc-buildtest/

Why buildtest?
---------------

Read https://buildtest.readthedocs.io/en/latest/what_is_buildtest.html to understand why we need buildtest and what we
are trying to solve.

Documentation
-------------

buildtest `documentation <http://buildtest.readthedocs.io/en/latest/>`_  is your source for getting help with buildtest.
If you get stuck check out the `current issues <https://github.com/HPC-buildtest/buildtest-framework/issues>`_ to see
if you face similar issue. If all else fails please create a ticket.

Source Code
------------

buildtest source code is under ``buildtest`` directory found in the root of this repository. The documentation  
is under ``docs`` which consist of ``Makefile`` and ``conf.py`` to build the sphinx project along with documentation
pages in **R**e**S**tructured**T**ext (rst). The regression test are found in top-level directory named ``tests`` and
the test suite is run via pytest.

Slack
------

Click the `Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_ to get in touch with the buildtest community.
If you already have an account then access the Slack Channel `here  <https://hpcbuildtest.slack.com>`_

Contributing Back
-------------------

We would love to get your contribution, if you are not sure check out the
`Contribution Guide <https://buildtest.readthedocs.io/en/latest/contributing.html>`_ to get started.

Author
-------

buildtest was founded by `Shahzeb Siddiqui <https://github.com/shahzebsiddiqui>`_ on Feb 24th 2017.

LICENSE
--------

buildtest is released under the MIT License. See
`LICENSE <https://github.com/HPC-buildtest/buildtest-framework/blob/master/LICENSE>`_ for more details
