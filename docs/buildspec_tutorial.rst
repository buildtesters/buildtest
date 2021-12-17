.. _writing_buildspecs:

Buildspec Tutorial
====================

.. toctree::
   :maxdepth: 1

   buildspecs/buildspec_overview
   buildspecs/global
   buildspecs/compiler
   buildspecs/spack
   buildspecs/advanced

Please proceed to :ref:`buildspec_overview` to get an overview of how to write buildspecs. This section can be done on your workstation.

.. _tutorial_setup:

Tutorials Setup
----------------

.. note::

    The tutorial setup is required if you want to run buildspecs using the the :ref:`compiler <compiler_schema>` and :ref:`spack <spack_schema>` schema.


To get started for this tutorial, you will need `docker <https://docs.docker.com/get-docker/>`_ on your machine to pull the container. You can pull the
container by running the following following::

    docker pull ghcr.io/buildtesters/buildtest_spack:latest

Next we can start an interactive shell into the container as follows::

    docker run -it ghcr.io/buildtesters/buildtest_spack:latest

We need to install buildtest and setup environment for this tutorial. This can be done as follows::

    git clone https://github.com/buildtesters/buildtest.git
    cd buildtest
    source scripts/spack_container/setup.sh

This container provides a software stack built with `spack <https://spack.readthedocs.io/en/latest/>`_, you should see
``buildtest``, ``spack`` and ``module`` command in your path. The configuration file used for this container is set via `BUILDTEST_CONFIGFILE`.

.. code-block::

    spack@ef50085c8a81:~/buildtest$ which spack
    /home/spack/spack/bin/spack

    spack@ef50085c8a81:~/buildtest$ which buildtest
    /home/spack/buildtest/bin/buildtest

    spack@ef50085c8a81:~/buildtest$ module --version

    Modules based on Lua: Version 8.3  2020-01-27 10:32 -06:00
        by Robert McLay mclay@tacc.utexas.edu

    (buildtest) spack@87354844bbf3:~/buildtest$ echo $BUILDTEST_CONFIGFILE
    /home/spack/buildtest/buildtest/settings/spack_container.yml