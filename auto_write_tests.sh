#!/bin/bash
script_dir="./docs/scripts"

tee $script_dir/buildtest-help.txt <<<"buildtest --help" | bash >> $script_dir/buildtest-help.txt

# Show Subcommand
tee $script_dir/buildtest-show-help.txt <<<"buildtest show --help" | bash >> $script_dir/buildtest-show-help.txt
tee $script_dir/buildtest-show-configuration.txt <<<"buildtest show -c" | bash >> $script_dir/buildtest-show-configuration.txt
tee $script_dir/buildtest-show-key.txt <<<"buildtest show -k singlesource" | bash >> $script_dir/buildtest-show-key.txt

# build Subcommand
tee $script_dir/buildtest-build-help.txt <<<"buildtest build --help" | bash >> $script_dir/buildtest-build-help.txt
tee $script_dir/coreutils-binary-test.txt <<<"buildtest build --package coreutils" | bash >> $script_dir/coreutils-binary-test.txt

tee $script_dir/build-compilers-suite.txt <<<"buildtest build -S compilers" |bash>> $script_dir/build-compilers-suite.txt
tee $script_dir/run-compilers-suite.txt <<<"buildtest run -S compilers"|bash>> $script_dir/run-compilers-suite.txt

tee $script_dir/build-openmp-suite.txt <<<"buildtest build -S openmp" |bash>>$script_dir/build-openmp-suite.txt
tee $script_dir/run-openmp-suite.txt <<<"buildtest run -S openmp"| bash>>$script_dir/run-openmp-suite.txt


tee $script_dir/build-single-configuration.txt <<<"buildtest build -c compilers.helloworld.hello_gnu.yml -vv" | bash >>$script_dir/build-single-configuration.txt

tee $script_dir/build-single-configuration-module.txt <<<"ml eb/2019; ml GCC; buildtest build -c compilers.helloworld.hello_gnu.yml -vv" | bash >>$script_dir/build-single-configuration-module.txt

tee $script_dir/build-shell-csh.txt <<<"buildtest build -c compilers.helloworld.hello_gnu.yml --shell csh" | bash >>$script_dir/build-shell-csh.txt
tee $script_dir/build-shell-bash.txt <<<"BUILDTEST_SHELL=bash buildtest build -c compilers.helloworld.hello_gnu.yml" | bash >>$script_dir/build-shell-bash.txt

tee $script_dir/build-lmod-collection.txt <<<"buildtest build -c compilers.helloworld.hello_intel_fortran.yml -co intelmpi -vv" | bash >>$script_dir/build-lmod-collection.txt
tee $script_dir/build-module-permute.txt <<<" buildtest build -c  compilers.helloworld.hello_intel_fortran.yml --modules intel -vv" | bash >> $script_dir/build-module-permute.txt
tee $script_dir/build-module-all-permute.txt <<<"BUILDTEST_PARENT_MODULE_SEARCH=all buildtest build -c  compilers.helloworld.hello_intel_fortran.yml --modules vmd -vv" | bash >> $script_dir/build-module-all-permute.txt

# lsf example
tee $script_dir/build-lsf-example.txt <<<"buildtest build -c compilers.helloworld.hello_lsf.yml -vv""" | bash >>$script_dir/build-lsf-example.txt
# slurm example
tee $script_dir/build-slurm-example.txt <<<"buildtest build -c compilers.helloworld.hello_slurm.yml -vv""" | bash >>$script_dir/build-slurm-example.txt

# Run example
ml purge; ml DefaultModules shared slurm gcc; buildtest build -b
tee $script_dir/run_subcommand/gcc-7.2.0.txt <<<"buildtest run -s gcc/7.2.0""" | bash >>$script_dir/run_subcommand/gcc-7.2.0.txt
ml purge; buildtest build -p gcc
tee $script_dir/run_subcommand/gcc.txt <<<"buildtest run -p gcc""" | bash >>$script_dir/run_subcommand/gcc.txt

# module collection
tee $script_dir/buildtest-module-collection-help.txt <<<"buildtest module collection -h """ | bash >>$script_dir/buildtest-module-collection-help.txt
ml purge; ml eb/2019 OpenMPI;
tee $script_dir/buildtest-module-collection-add.txt <<<"buildtest module collection -a """ | bash >>$script_dir/buildtest-module-collection-add.txt
tee $script_dir/buildtest-module-collection-list.txt <<<"buildtest module collection -l """ | bash >>$script_dir/buildtest-module-collection-list.txt

ml purge; ml shared mpich/ge/gcc/64/3.2.1; buildtest module collection -a
tee $script_dir/buildtest-module-collection-list-v2.txt <<<"buildtest module collection -l """ | bash >>$script_dir/buildtest-module-collection-list-v2.txt

ml purge; ml DefaultModules shared cmd; buildtest module collection -a
tee $script_dir/buildtest-module-collection-remove.txt <<<"buildtest module collection -r 2 """ | bash >>$script_dir/buildtest-module-collection-remove.txt

ml purge; ml DefaultModules shared cmd; buildtest module collection -a
ml purge; ml DefaultModules shared gcc;
tee $script_dir/buildtest-module-collection-list-before-update.txt <<<"buildtest module collection -l """ | bash >>$script_dir/buildtest-module-collection-list-before-update.txt
tee $script_dir/buildtest-module-collection-update.txt <<<"buildtest module collection -u 2 """ | bash >>$script_dir/buildtest-module-collection-update.txt
# MPI example
tee $script_dir/build-openmpi-example1.txt <<<"buildtest build -mc 0 -vv -c mpi.examples.hello.c.yml """ | bash >>$script_dir/build-openmpi-example1.txt
tee $script_dir/build-openmpi-example2.txt <<<"buildtest build -mc 0 -vv -c mpi.matrixmux.mm_mpi.f.yml """ | bash >>$script_dir/build-openmpi-example2.txt
tee $script_dir/build-mpich-example1.txt <<<"buildtest build -mc 1 -vv -c mpi.examples.hello.c.mpich.yml """ | bash >>$script_dir/build-mpich-example1.txt
tee $script_dir/build-srun-example1.txt <<<"buildtest build -mc 0 -vv -c mpi.examples.mpi_ping.c.slurm.yml """ | bash >>$script_dir/build-srun-example1.txt
# List Subcommand
tee $script_dir/buildtest-list-help.txt <<<"buildtest list --help" | bash >> $script_dir/buildtest-list-help.txt
tee $script_dir/buildtest-list-software.txt <<< "buildtest list --software" | bash >> $script_dir/buildtest-list-software.txt
tee $script_dir/buildtest-list-software-modules.txt <<< "buildtest list --modules" | bash >> $script_dir/buildtest-list-software-modules.txt
tee $script_dir/buildtest-list-easyconfigs.txt <<< "buildtest list --easyconfigs" | bash >> $script_dir/buildtest-list-easyconfigs.txt

# Find Subcommand
tee $script_dir/buildtest-find-help.txt <<<"buildtest find --help" | bash >> $script_dir/buildtest-find-help.txt
tee $script_dir/buildtest-find-test.txt <<<"buildtest find -ft all" | bash >> $script_dir/buildtest-find-test.txt

# TestConfigs Subcommand
tee $script_dir/buildtest-testconfigs-help.txt <<<"buildtest testconfigs --help" | bash >> $script_dir/buildtest-testconfigs-help.txt
tee $script_dir/buildtest-testconfigs-list.txt <<<"buildtest testconfigs list" | bash >> $script_dir/buildtest-testconfigs-list.txt
tee $script_dir/buildtest-testconfigs-view.txt <<<"buildtest testconfigs view mpi.matrixmux.mm_mpi.f.yml" | bash >> $script_dir/buildtest-testconfigs-view.txt

# Benchmark Subcommand
tee $script_dir/buildtest-benchmark-help.txt <<<"buildtest benchmark --help" | bash >> $script_dir/buildtest-benchmark-help.txt

# module commands 
tee $script_dir/buildtest-module-help.txt <<<"buildtest module --help" | bash >> $script_dir/buildtest-module-help.txt
tee $script_dir/module-load.txt <<<"buildtest module loadtest" | bash >> $script_dir/module-load.txt
#tee $script_dir/module-diff.txt <<<"buildtest module --diff-trees /clust/app/easybuild/2018/commons/modules/all,/usr/share/lmod/lmod/modulefiles/Core" | bash >> $script_dir/module-diff.txt
#tee $script_dir/module-diff-v2.txt <<< "buildtest module --diff-trees /clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all,/clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all" | bash >> $script_dir/module-diff-v2.txt
tee $script_dir/easybuild-modules.txt <<< "buildtest module --easybuild" | bash >> $script_dir/easybuild-modules.txt


tee $script_dir/easybuild-all-modules.txt <<< "BUILDTEST_SPIDER_VIEW=all buildtest module --easybuild" | bash >> $script_dir/easybuild-all-modules.txt
tee $script_dir/spack-modules.txt <<< "buildtest module --spack" | bash >> $script_dir/spack-modules.txt

tee $script_dir/spack-all-modules.txt <<< "BUILDTEST_SPIDER_VIEW=all buildtest module --spack" | bash >> $script_dir/spack-all-modules.txt

tee $script_dir/parent-module.txt <<< "buildtest module -d shared" | bash >> $script_dir/parent-module.txt

# status command
tee $script_dir/buildtest_status_help.txt <<< "buildtest status --help" | bash >> $script_dir/buildtest_status_help.txt
tee $script_dir/buildtest_status_report.txt <<< "buildtest status report " | bash >> $script_dir/buildtest_status_report.txt
tee $script_dir/buildtest_status_test.txt <<< "buildtest status test 0 " | bash >> $script_dir/buildtest_status_test.txt

tee $script_dir/module_tree_help.txt <<< "buildtest module tree -h" | bash >> $script_dir/module_tree_help.txt
tee $script_dir/module_tree_list.txt <<< "buildtest module tree -l" | bash >> $script_dir/module_tree_list.txt
tee $script_dir/module_tree_add.txt <<< "buildtest module tree -a /usr/share/lmod/lmod/modulefiles/Core" | bash >> $script_dir/module_tree_add.txt
tee $script_dir/module_tree_rm.txt <<< "buildtest module tree -r /usr/share/lmod/lmod/modulefiles/Core" | bash >> $script_dir/module_tree_rm.txt
tee $script_dir/module_tree_set.txt <<< "buildtest module tree -s /usr/share/lmod/lmod/modulefiles/Core" | bash >> $script_dir/module_tree_set.txt

