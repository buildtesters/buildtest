Managing Test Configuration
===========================

buildtest comes with many test configuration in markup language called YAML. These files have a **.yml** extension which
can be found in the repository in the top-level directory named **toolkit**.

buildtest has option to list, view and edit test configuration that can be accessed using ``buildtest testconfigs`` command.

Shown below is the usage


.. program-output:: cat scripts/buildtest-testconfigs-help.txt

Listing Test Configuration
-----------------------------

To view all test configuration in buildtest run the following::

    $ buildtest testconfigs list

This will report the name of test configuration and a brief description of the test. The first column represents the name of the test
which will be used if one wants to view or edit a test configuration.

.. program-output:: cat scripts/buildtest-testconfigs-list.txt


View and Edit Test Configuration
---------------------------------

If you want to view or edit a configuration you can use the following commands::

    $ buildtest testconfigs view <config>
    $ buildtest testconfigs edit <config>

In above command **<config>** represents the name of the test configuration as shown from ``builtest testconfigs list``.

For example, if let's view the content of test *mpi.matrixmux.mm_mpi.f.yml* by running::

    $ buildtest testconfigs view mpi.matrixmux.mm_mpi.f.yml

Shown below is the output of this file.

.. program-output:: cat scripts/buildtest-testconfigs-view.txt

Likewise, if you want to edit a test, use the **edit** subcommand and buildtest will launch an editor and open the file.
Currently, buildtest will use the **vim** editor for editing files.

To  edit the same test you will need to run::

      $ buildtest testconfigs edit mpi.matrixmux.mm_mpi.f.yml


