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

Alternately, you can configure BUILDTEST_MODULEPATH from command line. For more details see :ref:`module_tree_operation`

.. _configuring_spider:

Configure Spider View
---------------------

Lmod ``spider`` is used to retrieve module details in json format, this is done in buildtest during startup as follows::

    $ spider -o spider-json $BUILDTEST_MODULEPATH

The default configuration for ``spider_view`` is set to **current**  as shown below::

    module:
        spider_view: current

Valid values for spider_view are [``all``, ``current``].

If ``spider_view: all``, then buildtest will retrieve **all spider records** that includes all trees defined in
$BUILDTEST_MODULEPATH and any subtrees as a result. This is the default behavior of spider. For instance, if you have
two module trees ``/apps/modules/Compilers``, ``/apps/modules/MPI`` where ``/apps/modules/MPI`` is a sub-tree of
``/apps/modules/Compilers`` and you run the spider command as follows::

    spider -o spider-json /apps/modules/Compilers

The resulting output will retrieve modules from ``/apps/modules/MPI`` as well.

If you want to restrict the search of module retrieval to only trees defined in ``/apps/modules/Compilers`` and none of the
sub-trees then you must set ``spider_view: current``. This will instruct buildtest to only retrieve spider
records whose modulefile absolute path is a sub-directory of ``/apps/modules/Compilers``.

In the previous example, if ``spider_view: current`` and you run::

    spider -o spider-json /apps/modules/Compilers

Spider will retrieve records from both trees (``/apps/modules/Compilers``, ``/apps/modules/MPI``), but buildtest will
check if absolute path to modulefile is part of sub-directory (``/apps/modules/Compilers``). Any record from ``/apps/modules/MPI``
will be ignored.

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


The defualt will go to the testdir in your build test home at ``$HOME/.buildtest/testdir``

.. Note:: Shell expansion should work when specifying directories

Configuring Editor
-------------------

The EDITOR key will control which editor to use when editing files, this is used
in buildtest for instance when you want to edit files such as test configuration or
buildtest configuration::

    buildtest config edit
    buildtest testconfigs edit <test-configuration>

This will open the configuration in editor. The default value for **EDITOR** is
``vim`` but it can be changed to your editor of choice.

Currently, the following editors are available

- vim
- emacs
- nano

