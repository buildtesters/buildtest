buildtest - Software Testing Framework
=========================================

.. Note:: This project is under development, the official release will be in 2020.

Welcome to buildtest! **buildtest** is a framework for writing tests to conduct software stack testing for
HPC facilities. The goal of buildtest is to abstract test complexity such that a user can write test with minimal knowledge
of the system and the test is reusable between HPC sites. For more details on buildtest check :ref:`summary_of_buildtest`

This documentation was last rebuild on |today| and is intended for version |version|.

Introduction to buildtest
-------------------------

.. toctree::
   :glob:
   :maxdepth: 2

   what_is_buildtest.rst


Getting Started
---------------

.. toctree::
   :maxdepth: 2

   setup.rst
   configuring_buildtest.rst
   how_to_use_buildtest.rst
   command_reference.rst

Subcommands
-----------------

.. toctree::
   :maxdepth: 2

   list_subcommand.rst
   find_subcommand.rst
   module_subcommand.rst
   build_subcommand.rst
   run_subcommand.rst
   benchmark_subcommand.rst
   yaml_subcommand.rst
   show_subcommand.rst


Miscellaneous
--------------------

.. toctree::
    :maxdepth: 2

    easybuild_integration.rst
    ohpc_integration.rst
    contributing.rst
    references.rst

Useful Links
-------------

* buildtest-framework_ - The buildtest Testing framework
* buildtest-configs_ - buildtest YAML configs for generic apps


Slack
------

Click `Join <https://hpcbuildtest.herokuapp.com/>` the Slack Channel to get connected with the community. The slack
url is http://hpcbuildtest.slack.com


.. _buildtest-framework: https://github.com/HPC-buildtest/buildtest-framework
.. _buildtest-configs: https://github.com/HPC-buildtest/buildtest-configs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
