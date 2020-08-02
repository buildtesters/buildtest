Introspection Operation
=========================

Config Options (``buildtest config --help``)
-----------------------------------------------

.. program-output:: cat docgen/buildtest_config_--help.txt

The ``buildtest config`` command allows user to see view or edit your buildtest
settings file (``settings.yml``). To see content of your buildtest settings run::

    buildtest config view

Shown below is an example output.

.. program-output:: cat docgen/config-view.txt

Likewise, you can edit the file by running::

    buildtest config edit

To check if your buildtest settings is valid, run ``buildtest config validate``.
This will validate your ``settings.yml`` with the schema **settings.schema.json**.
The output will be the following.

.. program-output:: cat docgen/config-validate.txt

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates there was an error
on ``editor`` key in **config** object which expects the editor to be one of the
enum types [``vi``, ``vim``, ``nano``, ``emacs``]::

    $ buildtest config validate
    Traceback (most recent call last):
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/bin/buildtest", line 11, in <module>
        load_entry_point('buildtest', 'console_scripts', 'buildtest')()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 32, in main
        check_settings()
      File "/Users/siddiq90/Documents/buildtest/buildtest/config.py", line 71, in check_settings
        validate(instance=user_schema, schema=config_schema)
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/lib/python3.7/site-packages/jsonschema/validators.py", line 899, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'gedit' is not one of ['vi', 'vim', 'nano', 'emacs']

    Failed validating 'enum' in schema['properties']['config']['properties']['editor']:
        {'default': 'vim',
         'enum': ['vi', 'vim', 'nano', 'emacs'],
         'type': 'string'}

    On instance['config']['editor']:
        'gedit'


You can get a summary of buildtest using ``buildtest config summary``, this will
display information from several sources into one single command along.

.. program-output:: cat docgen/config-summary.txt


Schemas (``buildtest schema``)
-------------------------------

The ``buildtest schema`` command can show you list of available schemas just run
the command with no options and it will show all the json schemas buildtest supports.

.. program-output:: cat docgen/schemas/avail-schemas.txt

Shown below is the command usage of ``buildtest schema``

.. program-output:: cat docgen/buildtest_schema_--help.txt

The json schemas are hosted on the web at https://buildtesters.github.io/schemas/.
buildtest provides a means to display the json schema from the buildtest interface.
Note that buildtest will show the schemas provided in buildtest repo and not
ones provided by `schemas <https://github.com/buildtesters/schemas>`_ repo. This
is because, we let development of schema run independent of the framework.


Test Reports (``buildtest report``)
-------------------------------------

buildtest keeps track of all test results which can be retrieved via
**buildtest report**. Shown below is command usage.

.. program-output:: cat docgen/buildtest_report_--help.txt

You may run ``buildtest report`` and buildtest will display report
with default format fields.

.. program-output:: cat docgen/report.txt

There are more fields captured in the report, so if you want to see a
list of available format fields run ``buildtest report --helpformat``.

.. program-output:: cat docgen/report-helpformat.txt

You can filter report using ``--format`` field which expects field
name separated by comma (i.e **--format <field1>,<field2>**). In this example
we format by fields ``--format name,type,executor,state,returncode``

.. program-output:: cat docgen/report-format.txt

.. _buildtest_repo:

Managing Repositories
----------------------

.. program-output:: cat docgen/buildtest_repo_--help.txt

buildtest allows you to pull in any Github repository hosted on https://github.com.
buildtest doesn't come with any tests, therefore users are encouraged to
manage tests in their repositories and pull in their repos into buildtest via
``buildtest repo`` command.

Adding Repository
-------------------

To clone a git repository use ``buildtest repo add <url>``::

    $ buildtest repo add https://github.com/buildtesters/tutorials.git
    Cloning into '/Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials'...
    remote: Enumerating objects: 106, done.
    remote: Counting objects: 100% (106/106), done.
    remote: Compressing objects: 100% (73/73), done.
    remote: Total 106 (delta 32), reused 97 (delta 25), pack-reused 0
    Receiving objects: 100% (106/106), 20.97 KiB | 5.24 MiB/s, done.
    Resolving deltas: 100% (32/32), done.


The tests are organized by their namespace, meaning that you'll find GitHub
repos organized under github.com, then the organization or username, and then
the repository name.

The repos are stored in ``$HOME/.buildtest/site/github.com``

For example we can clone ``tutorials`` and ``buildtest-stampede2`` as follows::

    buildtest repo add https://github.com/buildtesters/tutorials.git
    buildtest repo add https://github.com/buildtesters/buildtest-stampede2.git

This will store the ``tutorials`` and ``buildtest-stampede2`` repo in directory
``buildtesters`` which is the organization name. Shown below is a directory layout
of the two clones::

    $ tree -L 2 $HOME/.buildtest/site/github.com
    /u/users/ssi29/.buildtest/site/github.com
    └── buildtesters
        ├── buildtest-stampede2
        └── tutorials

    3 directories, 0 files


If you try to clone a repo with folder that already exists, you'll be told the following::

    $ buildtest repo add https://github.com/buildtesters/tutorials.git
    /Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials already exists. Remove and try again.

You can also clone a specific branch via ``-b`` option as follows::

    $ buildtest repo add -b add/hello-world-test https://github.com/buildtesters/tutorials.git

Listing Available Repositories
-------------------------------

buildtest will track all repos added by ``buildtest repo add`` in a file
``$HOME/.buildtest/repo.yaml``. This file keeps track of all clone repos
and location where they are installed.

To get listing of all available repos you can run ``buildtest repo list``::

    $ buildtest repo list
    buildtesters/tutorials

You can see repository details by running::

    $ buildtest repo list -s
    buildtesters/tutorials:
      branch: master
      dest: /Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials
      state: enabled
      url: https://github.com/buildtesters/tutorials.git

This will show the content of the repo file ``$HOME/.buildtest/repo.yaml``.

Removing Repository
--------------------

To remove a repository from buildtest, use ``buildtest repo rm <repo>``. For
example, we can remove the current repository as follows::

    $ buildtest repo rm buildtesters/tutorials
    Removing Repository: buildtesters/tutorials and deleting files from /Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials

This will remove the repo from filesystem and remove entry from ``repo.yaml``.