#!/bin/bash
testdir="auto"
message()
{
    if [ $? == 0 ]; then
        echo "Running Command: $cmd         SUCCESS"
    else
        echo "Running Command: $cmd         FAILED"
    fi

}

cmd="buildtest --help"
$cmd &> ${testdir}/help.txt
message

cmd="buildtest -V"
$cmd &> ${testdir}/version.txt
message

cmd="buildtest list -s"
$cmd &> ${testdir}/list_software.txt
message

cmd="buildtest list -m"
$cmd &> ${testdir}/list_modules.txt
message

cmd="buildtest list -ec"
$cmd &> ${testdir}/easyconfigs.txt
message

cmd="buildtest find -ft all"
$cmd &> ${testdir}/find_all_test.txt
message

cmd="buildtest show -c"
$cmd &> ${testdir}/show_config.txt
message
cmd="buildtest show -k singlesource" &> ${testdir}/show_keys.txt
message

cmd="buildtest build -p gcc"
$cmd &> ${testdir}/build_gcc.txt
message 

cmd="buildtest --logdir /tmp build -p gcc"
$cmd &> ${testdir}/build_gcc_v2.txt
message 

cmd="buildtest build -S compilers" 
$cmd &> ${testdir}/compilers.txt
message 
cmd="buildtest run -S compilers"
$cmd &>> ${testdir}/compilers.txt
message

cmd="buildtest build -S openmp"
$cmd &> ${testdir}/openmp.txt
message

cmd="buildtest run -S openmp"
$cmd &>> ${testdir}/openmp.txt
message

# single configuration test
cmd="buildtest build -c compilers.helloworld.hello_gnu.yml"
$cmd &> ${testdir}/single_test.txt
message


cmd="buildtest build -c compilers.helloworld.hello_gnu.yml -co gcc730"
$cmd &> ${testdir}/single_test_collection.txt
message

cmd="buildtest build -c compilers.helloworld.hello_gnu.yml -m gcc"
$cmd &> ${testdir}/single_test_permute.txt
message

# testing csh test creation
cmd="buildtest build -s GCCcore/7.3.0-2.30 --shell csh"
$cmd &> ${testdir}/gcccore_6.4.0_csh.txt
message

cmd="buildtest module loadtest"
$cmd &> $testdir/moduleload.txt
message

cmd="buildtest module --spack"
$cmd &> $testdir/spack_modules.txt
message

cmd="BUILDTEST_SPIDER_VIEW=all buildtest module --spack"
$cmd &> $testdir/all_spack_modules.txt
message

cmd="buildtest module --easybuild"
$cmd &> $testdir/easybuild_modules.txt
message

cmd="BUILDTEST_SPIDER_VIEW=all buildtest module --easybuild"
$cmd &> $testdir/all_easybuild_modules.txt
message

cmd="buildtest module tree -a /usr/share/lmod/lmod/modulefiles/Core"
$cmd &> $testdir/add_module_tree.txt
message


cmd="buildtest module tree -r /usr/share/lmod/lmod/modulefiles/Core"
$cmd &> $testdir/rm_module_tree.txt
message

cmd="buildtest module tree -l "
$cmd &> $testdir/list_module_tree.txt
message

# running benchmark
cmd="buildtest benchmark osu -r" 
#$cmd &> ${testdir}/osu.txt
#message
