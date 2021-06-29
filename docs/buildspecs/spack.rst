.. _spack_schema:

Spack Schema
=============

.. Note:: This feature is in active development.


buildtest can generate tests for the `spack <https://spack.readthedocs.io/en/latest/>`_ package manager which can be
used if you want to install or test packages as part of a repeatable process. You must set ``type: spack`` property
in buildspec to use the spack schema for validating the buildspec test. Currently, we have
`spack-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/spack-v1.0.schema.json>`_
JSON schema that defines the structure of how tests are to be written in buildspec. Shown below is the schema header. The
**required** properties are ``type``, ``executor`` and ``spack``.

.. code-block:: json

      "$id": "spack-v1.0.schema.json",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "spack schema version 1.0",
      "description": "The spack schema is referenced using ``type: spack`` which is used for generating tests using spack package manager",
      "type": "object",
      "required": [
        "type",
        "executor",
        "spack"
      ],

Install Specs
---------------

Let's start off with a simple example where we create a test that can ``spack install zlib``. Shown below
is a test named **install_zlib**. The **spack** keyword is a JSON object, in this test we define the root
of spack using the ``root`` keyword which informs buildtest where spack is located. buildtest will automatically
check the path and source the startup script. Next we see the keyword ``install`` which is a JSON object which
contains a field ``specs`` which is a list of spack specs to install. The ``specs`` is property is a list of string types
and each item will added as a separate command as follows: ``spack install <spec>``

The schema is designed to mimic spack commands which will be clear with more examples.

.. program-output:: cat ../tutorials/spack/install_zlib.yml

If you build this test and inspect the generated script, buildtest will source spack
startup script - **source $SPACK_ROOT/share/spack/setup-env.sh** based on the ``root`` property. In this example,
we have spack cloned in **$HOME/spack** which is **/Users/siddiq90/spack** and buildtest will find the
startup script which is in ``share/spack/setup-env.sh``.

.. code-block:: shell

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack install  zlib

Spack Environment
-----------------

buildtest can generate scripts to make use of `spack environments <https://spack.readthedocs.io/en/latest/environments.html>`_ which
can be useful if you want to install or test specs in an isolated environment.

Currently, we can create spack environment (``spack env create``) via name, directory and manifest file (``spack.yaml``, ``spack.lock``) and pass any
options to **spack env create** command. Furthermore, we can activate existing spack environment via name or directory using
``spack env activate`` and pass options to the command.

Activate Spack Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

In this next example, we will activate an existing environment ``m4`` and add spec for **m4** and concretize the spack environment.
The ``env`` is an object that mimics the ``spack env`` command. The ``activate`` field maps to ``spack env activate`` command.
The **name** property is of ``type: string`` which is name of spack environment you want to activate. The ``specs`` property in **env** section
maps to ``spack add <specs`` instead of ``spack install``.

The property ``concretize: true`` will run ``spack concretize`` command that is only available as part of the ``env`` object since this command
is only applicable in spack environments.

.. program-output:: cat ../tutorials/spack/concretize_m4.yml

If we build this test and inspect the generated test we see that spack will activate a spack environment **m4**, add specs in spack
environment via ``spack add m4`` and concretize the environment. The ``concretize`` is a boolean type, if its ``true`` we will run ``spack concretize -f``,
if its ``false`` this command will not be in script.

.. code-block:: shell

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env activate  m4
    spack add m4
    spack concretize -f

If we inspect the output file we see that m4 was concretized in the spack environment.

.. code-block:: shell

    ==> Package m4 was already added to m4
    ==> Concretized m4
    [+]  volmsbn  m4@1.4.19%apple-clang@11.0.3+sigsegv arch=darwin-bigsur-skylake
    [+]  bc6kuc4      ^libsigsegv@2.13%apple-clang@11.0.3 arch=darwin-bigsur-skylake

Create a Spack Environment by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this next example, we will create a spack environment named ``m4_zlib`` that will install
`m4` and `zlib` spec. The **create** field is a JSON object that maps to ``spack env create``
command which can pass some arguments in the form of key/value pairs. The ``name`` property
in **create** section is used to create a spack environment by name.

The ``compiler_find: true`` is a boolean that determines if we need to find compilers in spack via
``spack compiler find``. This can be useful if you need to find compilers so spack can install specs
with a preferred compiler otherwise spack may have issues concretizing or install specs.
buildtest will run **spack compiler find** after sourcing spack.

.. note::
    The ``compiler_find`` option may not be useful if your compilers are already defined in
    one of your configuration scopes or ``spack.yaml`` that is part of your spack environment.

The ``option`` field can pass any command line arguments to ``spack install`` command
and this field is available for other properties.

.. program-output:: cat ../tutorials/spack/env_install.yml

If we build this test and see generated test we see that buildtest will create a
spack environment `m4_zlib` and activate the environment, add **m4** and **zlib**,
concretize the environment and install the specs.

.. code-block:: shell

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack compiler find
    spack env create  m4_zlib
    spack env activate  m4_zlib
    spack add m4
    spack add zlib
    spack concretize -f
    spack install --keep-prefix


Now let's examine the output of this test, shown below is the summary of this test, as you can
see we have successfully installed **m4** and **zlib** in a spack environment ``m4_zlib``.

.. code-block:: shell
    :emphasize-lines: 16-24

    ==> Found no new compilers
    ==> Compilers are defined in the following files:
        /Users/siddiq90/.spack/darwin/compilers.yaml
    ==> Updating view at /Users/siddiq90/spack/var/spack/environments/m4_zlib/.spack-env/view
    ==> Created environment 'm4_zlib' in /Users/siddiq90/spack/var/spack/environments/m4_zlib
    ==> You can activate this environment with:
    ==>   spack env activate m4_zlib
    ==> Adding m4 to environment m4_zlib
    ==> Adding zlib to environment m4_zlib
    ==> Concretized m4
    [+]  volmsbn  m4@1.4.19%apple-clang@11.0.3+sigsegv arch=darwin-bigsur-skylake
    [+]  bc6kuc4      ^libsigsegv@2.13%apple-clang@11.0.3 arch=darwin-bigsur-skylake
    ==> Concretized zlib
     -   2hw3hzd  zlib@1.2.11%apple-clang@11.0.3+optimize+pic+shared arch=darwin-bigsur-skylake
    ==> Updating view at /Users/siddiq90/spack/var/spack/environments/m4_zlib/.spack-env/view
    ==> Installing environment m4_zlib
    ==> Installing zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    ==> No binary for zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj found: installing from source
    ==> Fetching https://mirror.spack.io/_source-cache/archive/c3/c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1.tar.gz
    ==> No patches needed for zlib
    ==> zlib: Executing phase: 'install'
    ==> zlib: Successfully installed zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
      Fetch: 0.84s.  Build: 6.98s.  Total: 7.82s.
    [+] /Users/siddiq90/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    ==> Updating view at /Users/siddiq90/spack/var/spack/environments/m4_zlib/.spack-env/view

Creating Spack Environment from Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can create spack environment from a directory using the ``dir`` property that
is available as part of ``create`` and ``activate`` field. In this next example we
create a spack environment in our $HOME directory and concretize **m4** in the spack
environment

.. program-output:: cat ../tutorials/spack/env_create_directory.yml

When creating spack environment using directory, buildtest will automatically add the
``-d`` option which is required when creating spack environments. However, one can also pass
this using the ``option`` field. Shown below is the generated script for the above test.

.. code-block:: shell
    :emphasize-lines: 3-4

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env create  -d /Users/siddiq90/spack-envs/m4
    spack env activate  -d /Users/siddiq90/spack-envs/m4
    spack add m4
    spack concretize -f

buildtest will create environment first followed by activating the spack environment.

Create Spack Environment from Manifest File (spack.yaml, spack.lock)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack can create environments from `spack.yaml` or `spack.lock` which can be useful if you
already have a spack configuration that works for your system. When you are creating a spack
environment, you can use the ``manifest`` property to specify path to your ``spack.yaml`` or ``spack.lock``.
buildtest will not enforce that manifest names be **spack.yaml** or **spack.lock** since spack allows
one to create spack environment from arbitrary name so long as it is a valid spack configuration.

Shown below is an example buildspec that generates a test from a manifest file. The ``manifest`` property
is of ``type: string`` and this is only available as part of ``create`` property.

.. program-output:: cat ../tutorials/spack/env_create_manifest.yml

If we build this test and inspect the generated script we see ``spack env create`` command
will create an environment **manifest_example** using the manifest file that we provided.

.. code-block:: shell
    :emphasize-lines: 3

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env create  manifest_example /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/spack/example/spack.yaml
    spack env activate  manifest_example
    spack concretize -f

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

.. program-output:: cat ../tutorials/spack/pre_post_cmds.yml

If we build this test and inspect the generated script we see the following

.. code-block:: shell
    :emphasize-lines: 4-8,15-18

    #!/bin/bash


    ######## START OF PRE COMMANDS ########
    cd /tmp
    git clone https://github.com/spack/spack

    ######## END OF PRE COMMANDS   ########


    source /private/tmp/spack/share/spack/setup-env.sh
    spack install  zlib


    ######## START OF POST COMMANDS ########
    spack find
    rm -rf $SPACK_ROOT
    ######## END OF POST COMMANDS   ########

If we inspect the output, we see that `zlib` is installed as shown in output from ``spack find``

.. code-block:: shell
    :emphasize-lines: 9-10

    ==> Installing zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    ==> No binary for zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj found: installing from source
    ==> Fetching https://mirror.spack.io/_source-cache/archive/c3/c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1.tar.gz
    ==> No patches needed for zlib
    ==> zlib: Executing phase: 'install'
    ==> zlib: Successfully installed zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
      Fetch: 0.50s.  Build: 5.90s.  Total: 6.40s.
    [+] /private/tmp/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    -- darwin-bigsur-skylake / apple-clang@11.0.3 -------------------
    zlib@1.2.11