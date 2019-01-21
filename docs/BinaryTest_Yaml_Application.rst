.. _BinaryTest_Yaml_Application:

Building YAML configuration for binary testing for Software Packages (``_buildtest yaml --software``)
==========================================================================================================

In order to test binaries for software packages in HPC environment, buildtest
will assume there is a modulefile present and accessible via ``module`` command.
This implies the module tree is defined in ``MODULEPATH`` and ``BUILDTEST_MODULE_ROOT``.

When buildtest takes argument ``_buildtest yaml --software <module>`` it will run the
following command

.. code::

    module show <module>

buildtest will use the output of the above command to figure out root of the
software directory, in particular it searches for ``prepend_path("PATH"``
string to figure out the directory where binaries will reside. buildtest will
search for all files in all directories defined by ``$PATH`` in module file

buildtest will only add files, not directories, and only add files with unique
sha256 sum to avoid adding unncessary commands. buildtest will ignore symlinks
as well.

To demonstrate an example lets see the following example

``_buildtest yaml --software GCCcore/6.4.0``

buildtest will search for $PATH in module file. In the case of this example, the modulefile
will update the ``$PATH`` with directory ``/clust/app/easybuild/2018/IvyBridge/redhat/7.3/software/GCCcore/6.4.0/bin``
so lets take a look at this directory.

.. code::

    (buildtest-0.5.0) [siddis14@adwnode1 buildtest-framework]$ ls -l /clust/app/easybuild/2018/IvyBridge/redhat/7.3/software/GCCcore/6.4.0/bin
    total 84585
    -rwxr-xr-x 4 hpcswadm hpcswadm 4578120 May  9 15:57 c++
    lrwxrwxrwx 1 hpcswadm hpcswadm       3 May  9 15:57 cc -> gcc
    -rwxr-xr-x 1 hpcswadm hpcswadm 4574200 May  9 15:57 cpp
    lrwxrwxrwx 1 hpcswadm hpcswadm       8 May  9 15:57 f77 -> gfortran
    lrwxrwxrwx 1 hpcswadm hpcswadm       8 May  9 15:57 f95 -> gfortran
    -rwxr-xr-x 4 hpcswadm hpcswadm 4578120 May  9 15:57 g++
    -rwxr-xr-x 3 hpcswadm hpcswadm 4570976 May  9 15:57 gcc
    -rwxr-xr-x 2 hpcswadm hpcswadm  148568 May  9 15:57 gcc-ar
    -rwxr-xr-x 2 hpcswadm hpcswadm  148528 May  9 15:57 gcc-nm
    -rwxr-xr-x 2 hpcswadm hpcswadm  148536 May  9 15:57 gcc-ranlib
    -rwxr-xr-x 1 hpcswadm hpcswadm 3147992 May  9 15:57 gcov
    -rwxr-xr-x 1 hpcswadm hpcswadm 2876328 May  9 15:57 gcov-dump
    -rwxr-xr-x 1 hpcswadm hpcswadm 3103472 May  9 15:57 gcov-tool
    -rwxr-xr-x 2 hpcswadm hpcswadm 4578752 May  9 15:57 gfortran
    -rwxr-xr-x 4 hpcswadm hpcswadm 4578120 May  9 15:57 x86_64-pc-linux-gnu-c++
    -rwxr-xr-x 4 hpcswadm hpcswadm 4578120 May  9 15:57 x86_64-pc-linux-gnu-g++
    -rwxr-xr-x 3 hpcswadm hpcswadm 4570976 May  9 15:57 x86_64-pc-linux-gnu-gcc
    -rwxr-xr-x 3 hpcswadm hpcswadm 4570976 May  9 15:57 x86_64-pc-linux-gnu-gcc-6.4.0
    -rwxr-xr-x 2 hpcswadm hpcswadm  148568 May  9 15:57 x86_64-pc-linux-gnu-gcc-ar
    -rwxr-xr-x 2 hpcswadm hpcswadm  148528 May  9 15:57 x86_64-pc-linux-gnu-gcc-nm
    -rwxr-xr-x 2 hpcswadm hpcswadm  148536 May  9 15:57 x86_64-pc-linux-gnu-gcc-ranlib
    -rwxr-xr-x 2 hpcswadm hpcswadm 4578752 May  9 15:57 x86_64-pc-linux-gnu-gfortran


You will notice some files have same sha256 sum which may not be important for testing purpose.

.. code::

    (buildtest) [siddis14@amrndhl1157 bin]$ sha256sum x86_64-pc-linux-gnu-c++
    95e52799e1e4e766c98f3c64e3d13920375d694a546ff8884ed73f5188b62113  x86_64-pc-linux-gnu-c++
    (buildtest) [siddis14@amrndhl1157 bin]$ sha256sum c++
    95e52799e1e4e766c98f3c64e3d13920375d694a546ff8884ed73f5188b62113  c++

buildtest will write the content in ``command.yaml`` which must be checked for further modification

.. code::

    (buildtest-0.5.0) [siddis14@adwnode1 buildtest-framework]$ _buildtest yaml --software GCCcore/6.4.0
    Please check YAML file  /home/siddis14/github/buildtest-configs/buildtest/ebapps/gcccore/6.4.0/command.yaml  and fix test accordingly



If we look at the content we will see following binaries have been added

.. program-output:: cat scripts/BinaryTest_Yaml_Application/command.yaml



The last step is to add any options (if applicable) required to run the binary command.
