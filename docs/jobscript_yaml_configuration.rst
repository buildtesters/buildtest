.. _Jobscript_yaml_configuration:


Configuring Job scripts from yaml configuration
===============================================

buildtest can generate job scripts for the test script from the same yaml
configuration. This feature may be useful for users interested in testing
their application in a parallel environment.

Configuring LSF job script
--------------------------

If you have LSF, you can use the **scheduler** key word and specify **jobslots**
which will convert your command into **#BSUB -n <JobSlots>**

.. code::

   name: mpi_mm.c
   source: mpi_mm.c
   mpi: enabled
   buildopts: -O2
   nproc: 4
   scheduler: "LSF"
   jobslots: 4


Configuring SLURM job script
----------------------------

In SLURM, the scheduler and jobslots value will convert to **#SBATCH -N <JobSlots>**

.. code::

   name: mpi_mm.f
   source: mpi_mm.f
   mpi: enabled
   buildopts: -O2
   nproc: 4
   scheduler: "SLURM"
   jobslots: 4


In the future, there will be more yaml key options to tweak job parameters.

By default job scripts will be created in the test directory. Shown below is an
example for building slurm job script using option ``--enable-job``

.. code::

    [siddis14@prometheus buildtest-framework]$ buildtest -s icc/2018.1.163-GCC-6.4.0-2.28 --enable-job
    Detecting Software:  icc/2018.1.163-GCC-6.4.0-2.28
    --------------------------------------------
    [STAGE 1]: Building Binary Tests
    --------------------------------------------
    Detecting Test Type: Software
    Processing Binary YAML configuration:  /home/siddis14/github/buildtest-configs/buildtest/ebapps/icc/2018.1.163/command.yaml

    Generating 24 binary tests
    Binary Tests are written in /tmp/buildtest-tests/ebapp/icc/2018.1.163-GCC-6.4.0-2.28/
    Writing Log file:  /tmp/buildtest/icc/2018.1.163-GCC-6.4.0-2.28/buildtest_11_11_07_08_2018.log

If you look at the directory you will see a **.slurm** job script for each test that
was created


.. code::

    [siddis14@prometheus buildtest-framework]$ ls -l /tmp/buildtest-tests/ebapp/icc/2018.1.163-GCC-6.4.0-2.28/
    total 196
    -rw-r--r-- 1 siddis14 amer 3500 Aug  7 11:11 CMakeLists.txt
    -rw-r--r-- 1 siddis14 amer   72 Aug  7 11:11 icc_-V.sh
    -rw-r--r-- 1 siddis14 amer  120 Aug  7 11:11 icc_-V.slurm
    -rw-r--r-- 1 siddis14 amer   73 Aug  7 11:11 icpc_-V.sh
    -rw-r--r-- 1 siddis14 amer  121 Aug  7 11:11 icpc_-V.slurm
    -rw-r--r-- 1 siddis14 amer   81 Aug  7 11:11 profmerge_-help.sh
    -rw-r--r-- 1 siddis14 amer  129 Aug  7 11:11 profmerge_-help.slurm
    -rw-r--r-- 1 siddis14 amer   79 Aug  7 11:11 which_codecov.sh
    -rw-r--r-- 1 siddis14 amer  127 Aug  7 11:11 which_codecov.slurm
    -rw-r--r-- 1 siddis14 amer   79 Aug  7 11:11 which_dbmerge.sh
    -rw-r--r-- 1 siddis14 amer  127 Aug  7 11:11 which_dbmerge.slurm
    -rw-r--r-- 1 siddis14 amer   85 Aug  7 11:11 which_gfx_sys_check.sh
    -rw-r--r-- 1 siddis14 amer  133 Aug  7 11:11 which_gfx_sys_check.slurm
    -rw-r--r-- 1 siddis14 amer   79 Aug  7 11:11 which_icc.cfg.sh
    -rw-r--r-- 1 siddis14 amer  127 Aug  7 11:11 which_icc.cfg.slurm
    -rw-r--r-- 1 siddis14 amer   80 Aug  7 11:11 which_icpc.cfg.sh
    -rw-r--r-- 1 siddis14 amer  128 Aug  7 11:11 which_icpc.cfg.slurm
    -rw-r--r-- 1 siddis14 amer   87 Aug  7 11:11 which_libcilkrts.so.5.sh
    -rw-r--r-- 1 siddis14 amer  135 Aug  7 11:11 which_libcilkrts.so.5.slurm
    -rw-r--r-- 1 siddis14 amer   92 Aug  7 11:11 which_libintelremotemon.so.sh
    -rw-r--r-- 1 siddis14 amer  140 Aug  7 11:11 which_libintelremotemon.so.slurm
    -rw-r--r-- 1 siddis14 amer   93 Aug  7 11:11 which_loopprofileviewer.csh.sh
    -rw-r--r-- 1 siddis14 amer  141 Aug  7 11:11 which_loopprofileviewer.csh.slurm
    -rw-r--r-- 1 siddis14 amer   92 Aug  7 11:11 which_loopprofileviewer.sh.sh
    -rw-r--r-- 1 siddis14 amer  140 Aug  7 11:11 which_loopprofileviewer.sh.slurm
    -rw-r--r-- 1 siddis14 amer   80 Aug  7 11:11 which_map_opts.sh
    -rw-r--r-- 1 siddis14 amer  128 Aug  7 11:11 which_map_opts.slurm
    -rw-r--r-- 1 siddis14 amer   78 Aug  7 11:11 which_mcpcom.sh
    -rw-r--r-- 1 siddis14 amer  126 Aug  7 11:11 which_mcpcom.slurm
    -rw-r--r-- 1 siddis14 amer   87 Aug  7 11:11 which_offload_extract.sh
    -rw-r--r-- 1 siddis14 amer  135 Aug  7 11:11 which_offload_extract.slurm
    -rw-r--r-- 1 siddis14 amer   79 Aug  7 11:11 which_profdcg.sh
    -rw-r--r-- 1 siddis14 amer  127 Aug  7 11:11 which_profdcg.slurm
    -rw-r--r-- 1 siddis14 amer   89 Aug  7 11:11 which_profmergesampling.sh
    -rw-r--r-- 1 siddis14 amer  137 Aug  7 11:11 which_profmergesampling.slurm
    -rw-r--r-- 1 siddis14 amer   81 Aug  7 11:11 which_proforder.sh
    -rw-r--r-- 1 siddis14 amer  129 Aug  7 11:11 which_proforder.slurm
    -rw-r--r-- 1 siddis14 amer   79 Aug  7 11:11 which_tselect.sh
    -rw-r--r-- 1 siddis14 amer  127 Aug  7 11:11 which_tselect.slurm
    -rw-r--r-- 1 siddis14 amer   88 Aug  7 11:11 which_x86_64-linux.env.sh
    -rw-r--r-- 1 siddis14 amer  136 Aug  7 11:11 which_x86_64-linux.env.slurm
    -rw-r--r-- 1 siddis14 amer   80 Aug  7 11:11 which_xiar.cfg.sh
    -rw-r--r-- 1 siddis14 amer  128 Aug  7 11:11 which_xiar.cfg.slurm
    -rw-r--r-- 1 siddis14 amer   80 Aug  7 11:11 which_xild.cfg.sh
    -rw-r--r-- 1 siddis14 amer  128 Aug  7 11:11 which_xild.cfg.slurm
    -rw-r--r-- 1 siddis14 amer   73 Aug  7 11:11 xiar_-V.sh
    -rw-r--r-- 1 siddis14 amer  121 Aug  7 11:11 xiar_-V.slurm
    -rw-r--r-- 1 siddis14 amer   80 Aug  7 11:11 xild_--version.sh
    -rw-r--r-- 1 siddis14 amer  128 Aug  7 11:11 xild_--version.slurm

buildtest will create job scripts with the following extensions

* LSF job scripts will have extension **.lsf**
* SLURM job scripts will have extension **.slurm**



Generated SLURM Job
-------------------

::

    #!/bin/sh
    #SBATCH -N 1
    #SBATCH -q short
    #SBATCH -t 00:02
    module purge
    module load icc/2018.1.163-GCC-6.4.0-2.28
    icc -V


    Shown below is a generated LSF job script

Generated LSF Job
-----------------------

::

    #!/bin/sh
    #BSUB -n 1
    #BSUB -q short
    #BSUB -W 00:02
    module purge
    module load icc/2018.1.163-GCC-6.4.0-2.28
    icc -V
