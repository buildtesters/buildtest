Introspection Operation
=========================

Config Options (``buildtest config --help``)
______________________________________________

.. program-output:: cat docgen/buildtest_config_--help.txt

The ``buildtest config`` command allows user to see view or edit your buildtest settings file (``settings.yml``). You
can run ``buildtest config view`` to see the content of your buildtest settings as follows

.. program-output:: cat docgen/config-view.txt

Similarly, you can edit the configuration from the command line by running ``buildtest config edit`` which will open the
file in an editor (vim, emacs, nano).

If you want to reset the buildtest settings to the default settings, you can run ``buildtest config reset`` which will
overwrite your **settings.yml** with one provided by buildtest.

Shown below is an example

.. program-output:: cat docgen/config-reset.txt


.. _buildtest_get:

Get Options (``buildtest get --help``)
_______________________________________

.. program-output:: cat docgen/buildtest_get_--help.txt

buildtest can clone git repository via ``buildtest get`` that is used for cloning your buildtest test repositories in a
pre-determined location that buildtest can resolve when searching for Buildspecs.

The tests are organized by their namespace, meaning that you'll find GitHub repos organized under
github.com, then the organization or username, and then the repository name.

The repos are stored in ``$HOME/.buildtest/site/github.com``
which is organized by github organization followed by the repository name.

For example we can clone ``tutorials`` and ``buildtest-stampede2`` as follows::

    buildtest get https://github.com/buildtesters/tutorials.git
    buildtest get https://github.com/buildtesters/buildtest-stampede2.git

This will store the ``tutorials`` and ``buildtest-stampede2`` repo in directory ``buildtesters`` which is the organization
name. Shown below is a tree view after the two clones::

    (buildtest) ssi29@ag-mxg-hulk090> tree -L 2 $HOME/.buildtest/site/github.com
    /u/users/ssi29/.buildtest/site/github.com
    └── buildtesters
        ├── buildtest-stampede2
        └── tutorials

    3 directories, 0 files


If you try to clone a repo with folder that already exists, you'll be told the following::

    $ buildtest get https://github.com/buildtesters/tutorials.git
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials already exists. Remove and try again.

Clone Branches
----------------

You can also clone a specific branch via ``-b`` option as follows::

    $ buildtest get -b add/hello-world-test https://github.com/buildtesters/tutorials.git

Show Options (``buildtest show --help``)
_________________________________________

.. program-output:: cat docgen/buildtest_show_--help.txt


Show Schemas (``buildtest show schema``)
----------------------------------------------

buildtest can show json schema that is used for writing tests. This can be retrieved via
``buildtest show schema``. Shown below us the command usage

.. program-output:: cat docgen/buildtest_show_schema_--help.txt

The json schemas are hosted on the web at https://buildtesters.github.io/schemas/. buildtest provides
a means to display the json schema from the buildtest interface. Note that buildtest will show the schemas
provided in buildtest repo and not ones provided by `schemas <https://github.com/buildtesters/schemas>`_ repo. This
is because, we let development of schema run independent of the framework.

For example we can view the latest ``script`` schema as follows.

.. program-output:: cat docgen/script-schema.txt


