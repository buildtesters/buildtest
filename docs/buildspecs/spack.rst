.. Note:: Please see :ref:`tutorial_setup` before you proceed with this section

.. _buildtest_spack_integration:

Buildtest Spack Integration
============================

.. Note:: This feature is in active development.

buildtest can use `spack <https://spack.readthedocs.io/en/latest/>`_ to build test where one can use
spack to install packages followed by running any test. You must set ``type: spack``
in buildspec to use the spack schema for validating the buildspec test. Currently, we have
`spack.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/spack.schema.json>`_
JSON schema that defines the structure of how tests are to be written in buildspec. Shown below is the schema header. The
**required** properties are ``type``, ``executor`` and ``spack``.

.. literalinclude:: ../../buildtest/schemas/spack.schema.json
   :language: json
   :lines: 1-12

Install Specs
---------------

Let's start off with a simple example where we create a test that can ``spack install zlib``. Shown below
is a test named **install_zlib**. The **spack** keyword is a JSON object, in this test we define the root
of spack using the ``root`` keyword which informs buildtest where spack is located. buildtest will automatically
check the path and source the startup script. The ``install`` field is a JSON object that
contains a ``specs`` property which is a list of strings types that are name of spack packages to install. Each item in the
``specs`` property will be added as a separate ``spack install`` command. In the second test,
we run the same example except we clone spack and install zlib. When ``root`` property is not specified buildtest
will clone spack and automatically source the spack setup script (`source $SPACK_ROOT/share/spack/setup-env.sh`).

The schema is designed to mimic spack commands which will be clear with more examples.

.. literalinclude:: ../../examples/spack/install_specs.yml
    :language: yaml
    :emphasize-lines: 7-10

Let's build this test by running the following

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/install_specs.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/install_specs.txt


Let's inspect the generated script and output file via ``buildtest inspect query`` command. We notice that buildtest
will source spack setup script and install `zlib` which is automatically installed from the buildcache. In the second test
we clone spack and it will install zlib from source.

.. dropdown:: ``buildtest inspect query -o -t install_specs_example clone_spack_and_install_zlib``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/install_specs.txt

Spack Environment
-----------------

buildtest can generate scripts to make use of `spack environments <https://spack.readthedocs.io/en/latest/environments.html>`_ which
can be useful if you want to install or test specs in an isolated environment.

Currently, we can create spack environment (``spack env create``) via name, directory and manifest file (``spack.yaml``, ``spack.lock``) and pass any
options to **spack env create** command. Furthermore, we can activate existing spack environment via name or directory using
``spack env activate`` and pass options to the command. buildtest can remove spack environments automatically before creating spack environment
or one can explicitly specify by name.

Create a Spack Environment by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this next example, we will create a spack environment named ``m4_zlib`` that will install
`m4` and `zlib` spec. The **create** field is a JSON object that maps to ``spack env create``
command which can pass some arguments in the form of key/value pairs. The ``name`` property
in **create** section is used to create a spack environment by name. The ``activate`` property maps
to ``spack env activate`` command which is used to activate a spack environment. The **name** property is
of ``type: string`` which is name of spack environment you want to activate.

The ``compiler_find: true`` is a boolean that determines if we need to find compilers in spack via
``spack compiler find``. This can be useful if you need to find compilers so spack can install specs
with a preferred compiler otherwise spack may have issues concretizing or install specs.
buildtest will run **spack compiler find** after sourcing spack.

.. note::
    The ``compiler_find`` option may not be useful if your compilers are already defined in
    one of your configuration scopes or ``spack.yaml`` that is part of your spack environment.

The ``option`` field can pass any command line arguments to ``spack install`` command
and this field is available for other properties.

.. literalinclude:: ../../examples/spack/env_install.yml
    :language: yaml
    :emphasize-lines: 9-20

If we build this test and see generated test we see that buildtest will create a
spack environment `m4_zlib` and activate the environment, add **m4** and **zlib**,
concretize the environment and install the specs.

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/env_install.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/env_install.txt

.. dropdown:: ``buildtest inspect query -t install_in_spack_env``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/env_install.txt


Creating Spack Environment in Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can create spack environment from a directory using the ``dir`` property that
is available as part of ``create`` and ``activate`` field. In this next example we
create a spack environment in our $HOME directory and concretize **m4** in the spack
environment

.. literalinclude:: ../../examples/spack/env_create_directory.yml
    :language: yaml
    :emphasize-lines: 10-13

When creating spack environment using directory, buildtest will automatically add the
``-d`` option which is required when creating spack environments. However, one can also pass
this using the ``option`` field. Shown below is the build and generated script after running test.

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/env_create_directory.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/env_create_directory.txt

.. dropdown:: ``buildtest inspect query -o -t spack_env_directory``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/env_create_directory.txt

Create Spack Environment from Manifest File (spack.yaml, spack.lock)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack can create environments from `spack.yaml` or `spack.lock` which can be used if you
have a spack configuration that works for your system and want to write a buildspec. While creating a spack environment,
you can use the ``manifest`` property to specify path to your ``spack.yaml`` or ``spack.lock``.

.. note::
    buildtest will not enforce that manifest names be **spack.yaml** or **spack.lock** since spack allows
    one to create spack environment from arbitrary name so long as it is a valid spack configuration.

Shown below is an example buildspec that generates a test from a manifest file. The ``manifest`` property
is of ``type: string`` and this is only available as part of ``create`` property.

.. literalinclude:: ../../examples/spack/env_create_manifest.yml
    :language: yaml
    :emphasize-lines: 12

If we build this test and inspect the generated script we see ``spack env create`` command
will create an environment **manifest_example** using the manifest file that we provided from the spack.yaml.

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/env_create_manifest.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/env_create_manifest.txt

.. dropdown:: ``buildtest inspect query -o -t spack_env_create_from_manifest``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/env_create_manifest.txt

Removing Spack Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can remove spack environments which can be used if you are periodically running the same test where one is
creating the same environment. buildtest can automatically remove spack environment using the property ``remove_environment``
which will remove the environment before creating it with same name. This field is part of the ``create`` field and only works if
one is creating spack environments by name.

Alternately, buildtest provides the ``rm`` field which can be used for removing environment explicitly. In the ``rm``
field, the ``name`` is a required field which is the name of the spack environment to remove. The ``name`` field is of ``type: string``
Shown below are two example tests where we remove spack environment using the **remove_environment** and **rm** field.


.. literalinclude:: ../../examples/spack/remove_environment_example.yml
    :language: yaml
    :emphasize-lines: 11,27-28

Let's build this by running the following

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/remove_environment_example.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/remove_environment_example.txt


If we build and look at the generated te, we notice that spack will remove environments names: **remove_environment**, **dummy**.

.. dropdown:: ``buildtest inspect query -t remove_environment_automatically remove_environment_explicit``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/remove_environment_example.txt

Pre and Post Commands
----------------------

The spack schema supports ability to write arbitrary shell script content using the ``pre_cmds`` and ``post_cmds``
field that are of ``type: string`` and buildtest will insert the content into the test exactly as it is defined by
these two fields.

In this next example, we will test an installation of `zlib` by cloning spack from upstream and use ``pre_cmds`` field
to specify where we will clone spack. In this example, we will clone spack under **/tmp**. Since we don't have a valid
root of spack since test hasn't been run, we can ignore check for spack paths by specifying ``verify_spack: false`` which
informs buildtest to skip spack path check. Generally, buildtest will raise an exception if path specified by ``root`` is
invalid and if ``$SPACK_ROOT/share/spack/setup-env.sh`` doesn't exist since this is the file that must be sourced.

The ``pre_cmds`` are shell commands that are run before sourcing spack, whereas the ``post_cmds`` are run at the very
end of the script. In the `post_cmds`, we will ``spack find`` that will be run after ``spack install``.
We remove spack root (``$SPACK_ROOT``) so that this test can be rerun again.

.. literalinclude:: ../../examples/spack/pre_post_cmds.yml
    :language: yaml
    :emphasize-lines: 7-9,14-16

If we build this test and inspect the generated script we should get the following result.

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/pre_post_cmds.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/pre_post_cmds.txt

.. dropdown:: ``buildtest inspect query -o -t run_pre_post_commands``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/pre_post_cmds.txt

Configuring Spack Mirrors
--------------------------

We can add `mirrors <https://spack.readthedocs.io/en/latest/mirrors.html>`_ in the
spack instance or spack environment using the ``mirror`` property which is available
in the ``spack`` and ``env`` section. If the ``mirrror`` property is part of the ``env`` section, the
mirror will be added to spack environment. The ``mirror`` is an object that expects a Key/Value pair where
the key is the name of mirror and value is location of the spack mirror.

In this next example,  we will define a mirror name **e4s** that points to https://cache.e4s.io as the mirror location.
Internally, this translates to ``spack mirror add e4s https://cache.e4s.io`` command.

.. literalinclude:: ../../examples/spack/mirror_example.yml
    :language: yaml
    :emphasize-lines: 9-10,27-28

This test can be built by running::

    buildtest build -b $BUILDTEST_ROOT/examples/spack/mirror_example.yml

If we look at the generated script for both tests, we see that mirror is added for both tests. Note that
one can have mirrors defined in their ``spack.yaml`` or one of the `configuration scopes <https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes>`_
defined by spack.

.. dropdown:: ``buildtest inspect query -o  -t add_mirror add_mirror_in_spack_env``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/mirror_example.txt

Spack Test
-----------

.. Note:: ``spack test`` requires version `0.16.0 <https://github.com/spack/spack/releases/tag/v0.16.0>`_ or higher in order to use this feature.

buildtest can run tests using ``spack test run`` that can be used for testing installed specs with
tests provided by spack. In order to run tests, you need to declare the ``test`` section
which is of ``type: object`` in JSON and ``run`` is a required property. The ``run`` section maps to ``spack test run``
that is responsible for running tests for a list of specs that are specified using the ``specs`` property.

Upon running the tests, we can retrieve results using ``spack test results`` which is configured using the ``results``
property. The **results** property can query test results based via one of the following ways:

1. Spec Format: ``spack test results -- <spec>``
2. Suitename: ``spack test results <suitename>``


In example below we will test `m4` package by running ``spack test run m4`` and report the results with log file.

.. literalinclude:: ../../examples/spack/spack_test.yml
    :language: yaml
    :emphasize-lines: 9-13

If we look at the generated test, buildtest will install m4 followed by running the test. The **spack test run --alias**
option is used to reference name of suitename which can be used to reference suitename when using ``spack test results``
to search for test results. **buildtest will create a unique suite name for every run.**

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/spack_test.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/spack_test.txt

Take note of the suite name in generated test. By default spack creates a unique suite name when running `spack test run` but since this suitename
is not known in advance in-order to run `spack test results`, buildtest will take care of this for you.

.. dropdown:: ``buildtest inspect query -o -t spack_test_m4``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/spack_test.txt


We can search for test results using the spec format instead of suite name. In the ``results`` property we can
use ``specs`` field i to specify a list of spec names to run. In spack, you can retrieve
the results using ``spack test results -- <spec>``, note that double dash ``--`` is in front of spec name. We can
pass options to ``spack test results`` using the **option** property which is available for ``results`` and
``run`` property. Currently, spack will write test results in ``$HOME/.spack/tests`` and we can use ``spack test remove``
to clear all test results. This can be done in buildspec using the ``remove_tests`` field which
is a boolean. If this is set to **True** buildtest will run ``spack test remove -y`` to remove all test suites before running
the tests.

In this next example, we will create a spack environment to install `libxml2` and `libsigsegv` and test the package and report
log after running test.

.. literalinclude:: ../../examples/spack/spack_test_specs.yml
    :language: yaml
    :emphasize-lines: 17,20-22

We can build this test by running the following

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/spack_test_specs.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/spack_test_specs.txt

Now let's check the generated test and output file, we see buildtest will install **libxml2** and **libsigsegv**
in spack environment followed by removing all testsuites using ``spack test remove -y`` and run the test. Note that we can
query results in spec format (``spack test results --l --libxml2``) where spack will try to match a result file that matches the
corresponding spec.

.. dropdown:: ``buildtest inspect query -o -t spack_test_results_specs_format``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/spack_test_specs.txt


Specifying Scheduler Directives
---------------------------------

The spack schema supports all of the :ref:`scheduler scheduler directives <batch_support>` such
as ``sbatch``, ``bsub``, ``pbs``, ``cobalt``, and ``batch`` property in the buildspec.

The directives are applied at top of script. Shown below is a toy example that will define
directives using **sbatch** property. Note, this test won't submit job to scheduler
since we are not using the a slurm executor.

.. literalinclude:: ../../examples/spack/spack_sbatch.yml
    :language: yaml

buildtest will generate the shell script with the job directives and set the name, output and error
files based on name of test. If we build this test, and inspect the generated test we see that
**#SBATCH** directives are written based on the **sbatch** field.

.. dropdown:: ``buildtest inspect query -t spack_sbatch_example``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/spack_sbatch.txt

You can define :ref:`multiple executors <multiple_executors>` in your buildspec
with spack schema via ``executors``. This can be useful if you need to specify
different scheduler directives based on executor type since your executor will map to
a queue.

Shown below is an example buildspec that will specify ``sbatch`` directives for
``generic.local.sh`` and ``generic.local.bash``

.. literalinclude:: ../../examples/spack/spack_multiple_executor_sbatch.yml
  :language: yaml

