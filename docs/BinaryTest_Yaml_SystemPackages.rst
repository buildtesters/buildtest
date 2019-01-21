.. _BinaryTest_Yaml_SystemPackages:


Binary Test for System package (``_buildtest yaml --package``)
===================================================================

For system packages, typically you need to find all the binaries provided by the
system package. Let's assume for our discussion we are using Redhat. First you
would need to get an rpm listing of the files which can be done by running
``rpm -ql <package>``. While you go through each file you need to determine if file
is a binary executable with unique sha256sum. Once buildtest gets the binary listing, it
will run the ``which`` command against the binary file to test for file existence and write
this content to ``command.yaml`` file.

 This process can be tedious if done manually so buildtest has this automated in
 the framework. You may want to edit the file to run other options to test the binary
 that may include options like ``--help``, ``-h``, ``--version`` or ``-V``
 to check for a help or version check.

Since there is no universal test case for evaluating each binary we leave it up
to the users to determine how they want to perform binary test.

.. note:: The user needs to verify the YAML configuration after buidltest creates YAML file

To create a binary test for a system package, first check
``$BUILDTEST_CONFIGS_REPO/buildtest/system/<package>`` to see which system
package are already provided. If there is no directory then it makes sense to
create a the system package binary test using ``_buildtest list --package``

For this example we will generate the YAML configuration for  **firefox** package.

.. program-output:: cat scripts/BinaryTest_Yaml_SystemPackages/firefox_example.txt

buildtest will try to check for executable files in standard Linux path that include the following

 - /usr/bin
 - /bin
 - /sbin
 - /usr/sbin
 - /usr/local/bin
 - /usr/local/sbin

Looking at the content of yaml file we see the following

.. program-output:: cat scripts/BinaryTest_Yaml_SystemPackages/command.yaml


.. note:: Each item in **binaries** key will generate a separate test script and a new entry in CMakeList.txt

Once you have confirmed the test, you can share your YAML configuration by creating a Pull Request for the appropriate file.
