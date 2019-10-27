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

cmd="buildtest show -c"
$cmd &> ${testdir}/show_config.txt
message
cmd="buildtest show -k singlesource" &> ${testdir}/show_keys.txt
message

cmd="buildtest build -p gcc"
$cmd &> ${testdir}/build_gcc.txt
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
