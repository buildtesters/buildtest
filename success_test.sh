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

cmd="buildtest list -ls"
$cmd &> ${testdir}/list_software.txt
message

cmd="buildtest list -svr"
$cmd &> ${testdir}/list_modules.txt
message

cmd="buildtest list -ec"
$cmd &> ${testdir}/easyconfigs.txt
message

cmd="buildtest find -fc all"
$cmd &> ${testdir}/find_all_config.txt
message

cmd="buildtest find -ft all"
$cmd &> ${testdir}/find_all_test.txt
message

cmd="buildtest show -c"
$cmd &> ${testdir}/show_config.txt
message
cmd="buildtest show -k singlesource" &> ${testdir}/show_keys.txt
message

cmd="buildtest --clean-logs"
$cmd 
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
cmd="buildtest build -c /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml"
$cmd &> ${testdir}/single_test.txt
message

# testing csh test creation
cmd="buildtest build -s GCCcore/6.4.0 --shell csh"
$cmd &> ${testdir}/gcccore_6.4.0_csh.txt
message

# running benchmark
cmd="buildtest benchmark osu -r" 
$cmd &> ${testdir}/osu.txt
message
