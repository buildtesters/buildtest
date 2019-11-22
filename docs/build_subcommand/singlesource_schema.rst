Single Source YAML Schema
==========================

.. csv-table:: General Keys
    :header: "Key", "Required", "Type", "values","Description"
    :widths: 20,20,20,20,120

    **testtype**,``True``,``str``,``singlesource``,"Buildtest Class for Single Source Compilation"
    **description**,``True``,``str``,**N/A**,"Description Text for test configuration limited to 80 characters"
    **maintainer**,``True``,``list``,**N/A**,"List of Maintainers for the test"
    **scheduler**,``True``,``str``,"``local`` ``LSF`` ``SLURM``","Pick Scheduler Type"
    **mpi**,``False``,``bool``,"``False`` ``True``","Instruct buildtest if this test is a MPI test"
    **program**,``True``,``dict``,**N/A**,"Start of Program. This section where you specify test parameters."

.. csv-table:: Keys for ``program`` dictionary
    :header:   "Key", "Required", "Type", "values","Description"
    :widths:    20,20,20,20,80

    **source**,``True``,``str``,**N/A**,"Source File to compile. This file must be in ``src`` directory"
    **compiler**,``True``,``str``, "``gnu`` ``intel`` ``cuda``","Specify Compiler Name to detect compiler wrapper."
    **env**,``False``,``dict``,**N/A**,"Specify List of Environment Varaibles in Test"
    **cflags**,``False``,``str``,**N/A**,"Specify compiler flags to C compiler (i.e $CC)"
    **cxxflags**,``False``,``str``,**N/A**,"Specify compiler flags to C++ compiler (i.e $CXX)"
    **fflags**,``False``,``str``,**N/A**,"Specify compiler flags to Fortran compiler (i.e $FC)"
    **ldflags**,``False``,``str``,**N/A**,"Specify linker flags"
    **pre_build**,``False``,``str``,**N/A**,"Shell commands to run before building."
    **post_build**,``False``,``str``,**N/A**,"Shell commands to run after building."
    **pre_run**,``False``,``str``,**N/A**,"Shell commands to run before running executable."
    **post_run**,``False``,``str``,**N/A**,"Shell commands to run after running executable."
    **pre_exec**,``False``,``str``,**N/A**,"Command in front of executable."
    **post_exec**,``False``,``str``,**N/A**,"Commands after executable."
    **exec_opts**,``False``,``str``,**N/A**,"Passing options to executable."
    **bsub**,``False``,``dict``,**N/A**,"bsub block for specifying #BSUB directives in test."
    **sbatch**,``False``,``dict``,**N/A**,"sbatch block for specifying #SBATCH directives in test."
    **mpi**,``False``,``dict``,**N/A**,"MPI block for specifying mpi configuration."


.. csv-table:: Keys for ``program:bsub`` dictionary
    :header:   "Key", "Required", "Type", "Mapping","Description"
    :widths:    20,20,20,20,80

    **n**,``False``,``str``,``bsub -n``, "Equivalent to #BSUB -n"
    **M**,``False``,``str``,``bsub -M``, "Equivalent to #BSUB -M"
    **R**,``False``,``str``,``bsub -R``, "Equivalent to #BSUB -R"
    **q**,``False``,``str``,``bsub -q``, "Equivalent to #BSUB -q"
    **W**,``False``,``str``,``bsub -W``, "Equivalent to #BSUB -W"

.. csv-table:: Keys for ``program:sbatch`` dictionary
    :header:   "Key", "Required", "Type", "Mapping","Description"
    :widths:    20,20,20,20,80

    **n**,``False``,``str``,``sbatch -n``, "Equivalent to #SBATCH -n"
    **N**,``False``,``str``,``sbatch -N``, "Equivalent to #SBATCH -N"
    **mem**,``False``,``str``,``sbatch --mem``, "Equivalent to #SBATCH --mem"
    **C**,``False``,``str``,``sbatch -C``, "Equivalent to #SBATCH -C"
    **p**,``False``,``str``,``sbatch -p``, "Equivalent to #SBATCH -p"
    **t**,``False``,``str``,``sbatch -t``, "Equivalent to #SBATCH -t"

.. csv-table:: Keys for ``program:mpi`` dictionary
    :header:   "Key", "Required", "Type", "Values","Description"
    :widths:    20,20,20,20,80

    **flavor**,``False``,``str``,``openmpi`` ``mpich``, "Specify MPI Flavor. This is used to detect MPI wrapper."
    **launcher**,``False``,``str``,``mpirun`` ``mpiexec`` ``mpiexec.hydra``, "Specify the MPI Launcher to run MPI jobs"
    **launcher_opts**,``False``,``str``,**N/A**,"Pass options to MPI Launcher"


