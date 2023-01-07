Customize Shell
==================

Shell Type
-----------

buildtest will default to ``bash`` shell when running test, but we can configure shell
option using the ``shell`` field. The shell field is defined in schema as follows:

.. code-block:: json

    "shell": {
      "type": "string",
      "description": "Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The ``shell`` key can be used with ``run`` section to describe content of script and how its executed",
      "pattern": "^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|bash|sh|csh|tcsh|zsh|python).*"
    },

The shell pattern is a regular expression where one can specify a shell name along
with shell options. The shell will configure the `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_
in the test-script. In this example, we illustrate a few tests using different shell
field.

.. literalinclude:: ../tutorials/shell_examples.yml
   :language: yaml
   :emphasize-lines: 6,14,22,30,38

The generated test-script for buildspec **_bin_sh_shell** will specify shebang
**/bin/sh** because we specified ``shell: /bin/sh``:

.. code-block:: shell

    #!/bin/sh
    # Content of run section
    bzip2 --help

If you don't specify a shell path such as ``shell: sh``, then buildtest will resolve
path by looking in $PATH and build the shebang line.

In test **shell_options** we specify ``shell: "sh -x"``, buildtest will tack on the
shell options into the called script as follows:

.. code-block:: shell
    :emphasize-lines: 16

    #!/bin/bash


    ############# START VARIABLE DECLARATION ########################
    export BUILDTEST_TEST_NAME=shell_options
    export BUILDTEST_TEST_ROOT=/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.sh/shell_examples/shell_options/0
    export BUILDTEST_BUILDSPEC_DIR=/Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials
    export BUILDTEST_STAGE_DIR=/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.sh/shell_examples/shell_options/0/stage
    export BUILDTEST_TEST_ID=95c11f54-bbb1-4154-849d-44313e4417c2
    ############# END VARIABLE DECLARATION   ########################


    # source executor startup script
    source /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.sh/before_script.sh
    # Run generated script
    sh -x /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.sh/shell_examples/shell_options/0/stage/shell_options.sh
    # Get return code
    returncode=$?
    # Exit with return code
    exit $returncode


If you prefer **csh** or **tcsh** for writing scripts just set ``shell: csh`` or
``shell: tcsh``, note you will need to match this with appropriate executor. For now
use ``executor: generic.local.csh`` to run your csh/tcsh scripts. In this example below
we define a script using csh, take note of ``run`` section we can write csh style.

.. literalinclude:: ../tutorials/csh_shell_examples.yml
   :language: yaml

Customize Shebang
------------------

You may customize the shebang line in testscript using ``shebang`` field. This
takes precedence over the ``shell`` property which automatically detects the shebang
based on shell path.

In next example we have two tests **bash_login_shebang** and **bash_nonlogin_shebang**
which tests if shell is Login or Non-Login. The ``#!/bin/bash -l`` indicates we
want to run in login shell and expects an output of ``Login Shell`` while
test **bash_nonlogin_shebang** should run in default behavior which is non-login
shell and expects output ``Not Login Shell``. We match this with regular expression
with stdout stream.

.. literalinclude:: ../tutorials/shebang.yml
    :language: yaml

Now let's run this test as we see the following.

.. dropdown:: ``buildtest build -b tutorials/shebang.yml``

   .. command-output:: buildtest build -b tutorials/shebang.yml

If we look at the generated test for **bash_login_shebang** we see the shebang line
is passed into the script:

.. code-block:: shell
    :emphasize-lines: 1

    #!/bin/bash -l
    # Content of run section
    shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'

Python Shell
--------------

You can use **script** schema to write python scripts using the ``run`` property. In order to write python code you
must set ``shell`` property to python interpreter such as ```shell: python`` or full path to python wrapper such
as ``shell: /usr/bin/python``.

Here is a python example calculating area of circle

.. literalinclude:: ../tutorials/python-shell.yml
   :language: yaml


.. note::
    Python scripts are very picky when it comes to formatting, in the ``run`` section
    if you are defining multiline python script you must remember to use 2 space indent
    to register multiline string. buildtest will extract the content from run section
    and inject in your test script. To ensure proper formatting for a more complex python
    script you may be better off writing a python script in separate file and invoke the
    python script in the ``run`` section.