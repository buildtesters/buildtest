.. _global_schema:

Global Schema
==============

The global schema is validated with for all buildspecs is the top-level
schema when defining a buildspec file.

Please refer to `Global Schema Documentation <https://buildtesters.github.io/buildtest/pages/schemadocs/global.html>`_ that
provides a summary .

Schema Definition
--------------------------

Shown below is the start of the schema definition for  **global.schema.json**

.. literalinclude:: ../../buildtest/schemas/global.schema.json
   :lines: 1-8
   :language: json

This schema requires that every buildspec should have ``version`` and ``buildspecs`` fields. The
version key is required to lookup an a sub-schema using the ``type`` field.
The ``buildspecs`` is the start of test declaration.

Example Buildspec
------------------

.. literalinclude:: ../tutorials/hello_world.yml
   :language: yaml

The field ``version`` ``buildspecs`` and ``maintainers`` are validated with **global.schema.json**
using `jsonschema.validate <https://python-jsonschema.readthedocs.io/en/stable/_modules/jsonschema/validators/#validate>`_
method. The test section within ``hello_world`` is validated by sub-schema by looking up schema based
on ``type`` field.

Every sub-schema requires **type** field in this case, ``type: script`` informs
buildtest to validate with the :ref:`script_schema`. All type schemas have a version,
currently buildtest supports **1.0** version for all type schemas. The
``version: "1.0"`` is used to select the version of the sub-schema,
in this example we validate with the schema `script-v1.0.schema.json <https://buildtesters.github.io/buildtest/pages/schemas/script-v1.0.schema.json>`_.

To understand how buildtest validates the buildspec see :ref:`parsing buildspecs <parse_stage>`.

.. _maintainers:

Maintainers
--------------

The ``maintainers`` is an optional field that can be used to specify a list of test maintainers for a given buildspec.
The **maintainers** property is used by buildtest to report :ref:`buildspecs by maintainers <buildspec_maintainers>` when querying
buildspec cache. You can also :ref:`filter buildspecs <filter_buildspecs_with_buildtest_build>` by maintainers during
building via ``buildtest build --filter maintainers=<NAME>`` if one wants to filter tests


In this example, we have two maintainers ``@johndoe`` and ``@bobsmith``. The maintainers is a list of strings but must
be unique names, generally this can be your name or preferably a github or gitlab handle.

.. literalinclude:: ../tutorials/maintainers_example.yml
   :language: yaml

Test Names
-----------

The **buildspecs** property is a JSON object that defines one or more test. This
is defined in JSON as follows:

.. code-block:: json

    "buildspecs": {
      "type": "object",
       "description": "This section is used to define one or more tests (buildspecs). Each test must be unique name",
       "propertyNames": {
          "pattern": "^[A-Za-z_.][A-Za-z0-9_.]*$",
          "maxLength": 32
       }
    }

The test names take the following pattern ``"^[A-Za-z_.][A-Za-z0-9_.]*$"`` and limited
to 32 characters. In previous example, the test name is **hello_world**. You must have unique
testname in your **buildspecs** section, otherwise you will have an invalid buildspec
file. The ``description`` field is used to document the test and limited to 80 characters.

.. Note:: We refer to the entire YAML content as **buildspec file**, this is not to be confused with the **buildspecs** field.

Buildspec Structure
--------------------

Shown below is an overview of buildspec file. In this diagram we define one test within
``buildspecs`` property named ``systemd_default_target``. This test is using the
script schema defined by ``type: script``.  The ``executor`` property is a required
property that determines how test is run. The executors are defined in buildtest configuration
see :ref:`configuring_buildtest` for more details.

The ``run`` property is used for defining content of script, this can a shell-script
(bash,csh) or python script.

.. image:: ../_static/buildspec-structure.png

Please proceed to :ref:`buildspec_overview` to learn more about buildspecs.

