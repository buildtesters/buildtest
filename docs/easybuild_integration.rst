.. _EasyBuild_Integration:

Easybuild Integration
=========================

buildtest can determine if software is built by easybuild. To enable easybuild check
with buildtest you can set the variable ``BUILDTEST_EASYBUILD`` in your configuration file
as follows

::

    BUILDTEST_EASYBUILD: True

Declare this as an environment variable

::

    # bash/sh shell
    export BUILDTEST_EASYBUILD=True

    # csh/tcsh shell
    setenv BUILDTEST_EASYBUILD True

You may specify this option at command line ``-eb`` or long option ``--easybuild``. This option is available for build subcommand.

How buildtest checks for easybuild software
---------------------------------------------

In this example below buildtest detects ``gnu7/7.3.0`` is not a easybuild app.

::

    (buildtest) buildtest-framework[devel] $ buildtest build -s gnu7/7.3.0 --easybuild
    Detecting Software:  gnu7/7.3.0
    Application: gnu7/7.3.0 is not built from Easybuild, cannot find easyconfig file in installation directory

buildtest will do the following check

1. Run ``$LMOD_CMD bash show <module>`` where <module> is argument to ``-s``
2. Search for string ``prepend_path(PATH)`` in output from step 1
3. Check if directory exist that is added to PATH variable
4. Check if there is a sub-directory ``easybuild``
5. Check if there is an easyconfig inside the sub-directory.


buildtest can also return a list of easyconfigs from a module tree (``buildtest list --easyconfigs``).
For more details see :ref:`list_easyconfigs`

The implementation for easyconfig retrieval is very similar to how buildtest
checks if software is built by easybuild.
