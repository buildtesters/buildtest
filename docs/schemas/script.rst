Script Schema
==============

- Framework Schema File: https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/buildsystem/schemas/script/script-v0.0.1.schema.json
- Development Schema File: https://buildtesters.github.io/schemas/script/script-v0.0.1.schema.json

Description
------------

.. csv-table::
   :header: "Field", "Type", "Description"
   :widths: 20, 20, 60

   **type**, **string**, "The schema name to use. Must be ``type: script``"
   **run**, **string**, "A script to run using one of the supported shells"
   **shell**, **string**, "The shell field is used to control how test is created based on content in ``run`` field.
   The shell must adhere to the following patterns ``^(/bin/bash|/bin/sh|sh|bash|python).*``"
   **shebang**, **string**, "Customize the shebang in the testscript. By default, the shebang is used based on **shell** field but this can be tweaked using ``shebang``."
   **env**, **object**, "One or more key value pairs for an environment (key=value)"
   **description**, **string**, "A description for the build recipe"
   **executor**, **string**, "Specify the executor to use when running the test"
   **status**, **object**, "The status field is used for reporting how buildtest reports ``PASS`` or ``FAIL``.
   The status field can match result based on returncode or regex based on output or error stream."

status properties
------------------

.. csv-table::
    :header: "Field", "Type", "Description"
    :widths: 20, 20, 60

    **returncode**, **integer**, "Test will be ``PASS`` if test return code matches the value specified by field ``returncode``. By default a returncode of 0 is PASS and non-zero is FAIL"
    **regex**, **object**, "Match test based on regular expression using re.search"

regex properties
~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "Field", "Type", "Description"
    :widths: 20, 20, 60

    **stream**, **string**, "Select the stream to run the regular expression. This field can only take one of the two
    values: ``stdout`` ``stderr``. The regular expression will be evaluated based on output or error stream after
    test execution."
    **exp**, **string**, "Regular expression to use via ``re.search`` against the ``stream`` field"

