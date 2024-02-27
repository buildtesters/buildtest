Buildtest Tutorial on AWS
=========================

Setup
-----

This section of tutorial will be completed in `Amazon Web Services (AWS) <https://aws.amazon.com/>`_ environment. Once you have access to system,
please :ref:`installing_buildtest` and then proceed to the next section.

Once you are done, please run the following commands to ensure you are using the correct configuration file

.. code-block:: bash

    export BUILDTEST_CONFIGFILE=$BUILDTEST_ROOT/buildtest/settings/aws.yml
    buildtest config path

You can verify the configuration is valid by runnning the following::

    buildtest config validate

If you see no errors, then you are ready to proceed to the next section.

Hello World Compilation
-----------------------

Let's start off with a simple hello world compilation in C using the GNU compiler. We have the following buildspec
that will compile a code source code ``hello.c`` using the ``gcc`` compiler wrapper.

.. literalinclude:: ../../aws_tutorials/hello_world/hello_world.yml
    :language: yaml

The source code is the following

.. literalinclude:: ../../aws_tutorials/hello_world/hello.c
    :language: c

Let's try building this example and inspect the test results to see what happens.


