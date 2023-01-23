.. _buildspec_tutorial:

Buildspec Tutorial
====================

.. toctree::
   :maxdepth: 1

   buildspecs/buildspec_overview
   buildspecs/performance_checks
   buildspecs/compiler
   buildspecs/spack


Please proceed to :ref:`buildspec_overview` to get an overview of how to write buildspecs. This section can be done on your workstation.

.. _tutorial_setup:

Tutorials Setup
----------------

.. note::

    The tutorial setup is required if you want to run buildspecs using the the :ref:`compiler <compiler_schema>` and :ref:`spack <buildtest_spack_integration>` schema.


To get started for this tutorial, you will need `docker <https://docs.docker.com/get-docker/>`_ on your machine to pull the container. At NERSC,
you can use `podman <https://podman.io/>`_ or `shifter <https://github.com/NERSC/shifter>`_ to access the container, you will need to start an interactive shell.

.. tab-set::

    .. tab-item:: docker

        .. code-block:: console

            docker pull ghcr.io/buildtesters/buildtest_spack:latest
            docker run -it ghcr.io/buildtesters/buildtest_spack:latest /bin/bash --login


    .. tab-item:: podman

        .. code-block:: console

            podman pull ghcr.io/buildtesters/buildtest_spack:latest
            podman run -it ghcr.io/buildtesters/buildtest_spack:latest /bin/bash --login

    .. tab-item:: shifter

        .. code-block:: console

            shifter -E --image=registry.services.nersc.gov/siddiq90/buildtest_spack:latest -- /bin/bash --login

If you are using podman on Perlmutter, please do the following::

    mkdir -p $HOME/.config/containers
    touch $HOME/.config/containers/storage.conf

Next add the following content in `storage.conf`::


    [storage]
      driver = "overlay"
      graphroot = "/tmp/<USER>/storage"
      [storage.options]
        size = ""
        remap-uids = ""
        remap-gids = ""
        ignore_chown_errors = "true"
        remap-user = ""
        remap-group = ""
        mount_program = "/usr/bin/fuse-overlayfs"
        mountopt = ""

**Please update the path /tmp/<USER>/storage to your username.**

We need to install buildtest and setup environment for this tutorial. We recommend you clone buildtest in your HOME directory.
This can be done as follows::

    cd ~
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