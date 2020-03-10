.. _configuring_buildtest:

Configuring buildtest
======================


Configuration File
--------------------

buildtest will store the user's buildtest configuration at ``$HOME/.buildtest/settings.yml``. This file is responsible for
configuring buildtest which can be customized to fit your site requirements. buildtest will automatically
generate this file if it is not present. To view the buildtest configuration you can run the following::

    $ buildtest config view

Shown below is the user's buildtest configuration.

.. program-output:: cat docgen/buildtest_config_view.txt

buildtest keeps a backup configuration (``~/.buildtest/settings.yml.bak``) in case you want to restore to
the original settings. This can be done by running

.. program-output:: cat docgen/buildtest_config_restore.txt

Similarly, if you want to edit the configuration you may run::

    $ buildtest config edit

This will open the configuration in ``vim`` editor. For list of options on buildtest configuration, run
``buildtest config --help`` for more details.


Next section will discuss the variables defined in the configuration file.


Configuring Module Trees
--------------------------

**BUILDTEST_MODULEPATH** is a list of module tree in where your module files are found.

buildtest will read BUILDTEST_MODULEPATH to retrieve all the module files.

Let's assume we want to add ``/opt/apps`` and ``/workspace/apps`` as module trees to BUILDTEST_MODULEPATH. This can
be done in your configuration as follows::

	BUILDTEST_MODULEPATH:
        - /opt/apps
        - /workspace/apps

If you set an invalid directory path in ``BUILDTEST_MODULEPATH`` you will get
the following message

.. Error::
    /opt/apps directory does not exist, specified in BUILDTEST_MODULEPATH


If you don't specify a module tree for BUILDTEST_MODULEPATH then buildtest
will read the value of MODULEPATH.

Purging Modules In Tests
--------------------------

buildtest will automatically run ``module purge`` before loading modules in test
script. This is to avoid unexpected behaviors when user shell has modules
loaded in their shell session.

The configuration section in buildtest that defines module purge is shown below::

    build:
      module:
        purge:
          force: False

If you want to purge sticky modules, then consider setting ``force: True`` which will
invoke ``module --force purge`` at start of each test script. By default, this
is set to **False**.

Configure Test Directory
--------------------------

buildtest must write tests somewhere, in order to define a directory path, use the ``testdir`` key defined in ``build``
section. If you want to redirect tests to ``/tmp/$USERS/buildtest`` you can set that as follows::

    build:
        testdir: /tmp/$USERS/buildtest/


The default will go to the testdir in your build test home at ``$HOME/.buildtest/testdir``

.. Note:: Shell expansion should work when specifying directories

Configuring Editor
-------------------

The EDITOR key will control which editor to use when editing files, this is used
in buildtest for instance when you want to edit files such as test configuration or
buildtest configuration::

    buildtest config edit

This will open the configuration file in an editor. The default value for **EDITOR** is
``vim`` but it can be changed to your editor of choice.

Currently, the following editors are available

- vim
- emacs
- nano

