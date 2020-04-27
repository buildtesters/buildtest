Introspection Operation
=========================


Show Options (``buildtest show --help``)
_________________________________________

.. program-output:: cat docgen/buildtest_show_-h.txt


Show YAML Schema (``buildtest show schema``)
----------------------------------------------

buildtest can show json schema that is used for writing tests. This can be retrieved via
``buildtest show schema``. Shown below us the command usage::

    $ buildtest show schema --help
    usage: buildtest [options] [COMMANDS] show schema [-h] [-v VERSION] [-n NAME]

    optional arguments:
      -h, --help            show this help message and exit
      -v VERSION, --version VERSION
                            choose a specific version of schema to show.
      -n NAME, --name NAME  show schema by name (e.g., script)


The json schemas are hosted on the web at https://buildtesters.github.io/schemas/. buildtest provides
a means to display the json schema from the buildtest interface. Note that buildtest will show the schemas
provided in buildtest repo and not ones provided by `schemas <https://github.com/buildtesters/schemas>`_ repo. This
is because, we let development of schema run independent of the framework.

For example we can view the latest ``script`` schema as follows.

.. program-output:: cat docgen/buildtest_show_schema.txt


