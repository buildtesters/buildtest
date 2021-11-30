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


.. _tutorial_setup:

Tutorials Setup
----------------

To get started for this tutorial we will start an interactive shell in spack container for this exercise. We need
to bind mount $BUILDTEST_ROOT into the container in order to use buildtest inside the container.

.. code-block:: console

    docker run -it -v $BUILDTEST_ROOT:/home/spack/buildtest ghcr.io/buildtesters/buildtest_spack:latest


Next, lets source the setup script required for using buildtest inside the container

.. code-block:: console

    source $HOME/buildtest/scripts/spack_container/setup.sh

If everything is done correctly you will see ``buildtest``, ``spack`` and ``module`` command in your path

.. code-block::

    spack@ef50085c8a81:~/buildtest$ which spack
    /home/spack/spack/bin/spack

    spack@ef50085c8a81:~/buildtest$ which buildtest
    /home/spack/buildtest/bin/buildtest

    spack@ef50085c8a81:~/buildtest$ module --version

    Modules based on Lua: Version 8.3  2020-01-27 10:32 -06:00
        by Robert McLay mclay@tacc.utexas.edu
