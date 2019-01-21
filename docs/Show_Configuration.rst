.. _Show_Configuration:


Show Configuration (``_buildtest --show``)
=============================================

buildtest can display it's configuration by running ``_buildtest --show``. The
configuration can be changed by the following.

 1. Command Line
 2. Environment Variable (``BUILDTEST_``)
 3. Configuration File (``config.yaml``)

buildtest will read configuration from file ``config.yaml`` and override any configuration
by environment variables that start with ``BUILDTEST_``. The command line may
override the environment variables at runtime.

Shown below is a sample configuration from buildtest.


.. code::

    (buildtest) [siddis14@gorgon buildtest-framework]$ _buildtest --show
    Check Configuration
     buildtest configuration summary
     (C): Configuration File,  (E): Environment Variable
    BUILDTEST_CLEAN_BUILD                              (C) = False
    BUILDTEST_CONFIGS_REPO                             (C) = /home/siddis14/github/buildtest-configs
    BUILDTEST_EASYBUILD                                (C) = False
    BUILDTEST_EMAIL                                    (C) = True
    BUILDTEST_ENABLE_JOB                               (C) = True
    BUILDTEST_JOB_TEMPLATE                             (C) = /home/siddis14/github/buildtest-framework/template/job.slurm
    BUILDTEST_LOGDIR                                   (C) = /tmp/buildtest/logs
    BUILDTEST_MODULE_NAMING_SCHEME                     (C) = FNS
    BUILDTEST_MODULE_ROOT                              (C) = /clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all:/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all:/clust/app/easybuild/2018/commons/modules/all
    BUILDTEST_OHPC                                     (C) = False
    BUILDTEST_PERL_REPO                                (C) = /home/siddis14/github/Perl-buildtest-config
    BUILDTEST_PREPEND_MODULES                          (C) = []
    BUILDTEST_PYTHON_REPO                              (C) = /home/siddis14/github/Python-buildtest-config
    BUILDTEST_RUBY_REPO                                (C) = /home/siddis14/github/Ruby-buildtest-config
    BUILDTEST_RUN_DIR                                  (C) = /tmp
    BUILDTEST_R_REPO                                   (C) = /home/siddis14/github/R-buildtest-config
    BUILDTEST_SHELL                                    (C) = sh
    BUILDTEST_SUCCESS_THRESHOLD                        (C) = 1.0
    BUILDTEST_TESTDIR                                  (C) = /tmp/buildtest/tests




``_buildtest --show`` will update the output as you set any BUILDTEST environment
variables.

For instance, if you want to customize the buildtest log via environment variable. ``_buildtest --show`` will report
which values are overridden by environment variable with a notation **(E)**.

See example below

::

    (buildtest) [siddis14@gorgon buildtest-framework]$ export BUILDTEST_LOGDIR=/tmp
    (buildtest) [siddis14@gorgon buildtest-framework]$ _buildtest --show | grep BUILDTEST_LOGDIR
    BUILDTEST_LOGDIR                                   (E) = /tmp



.. Note:: if you plan to customize your buildtest configuration with configuration file
    and environment variable, always check your shell environment first to avoid having
    values overridden accidently
