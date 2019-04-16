############################################################################
#
#  Copyright 2017-2019
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################


import os
import stat
import subprocess
import time
import yaml

from datetime import datetime
from buildtest.tools.config import config_opts
from buildtest.tools.run import write_system_info

dict_keys1 = ["proc", "min_message_size", "max_message_size", "iter_msg_size",
              "max_mem_per_proc", "warmup_iter", "calls", "full_format"]
dict_keys2 = ["proc", "iter_msg_size", "warmup_iter", "calls", "full_format"]
dict_keys3 = ["iter", "warmup_iter"]
dict_keys4 = ["win_option", "sync_option", "warmup_iter", "iter"]
dict_keys5 = ["iter", "warmup_iter", "threads"]
dict_keys6 = ["proc", "iter", "warmup_iter"]

lookup_table = {
    "osu_allgather": dict_keys1,
    "osu_allgatherv": dict_keys1,
    "osu_allreduce": dict_keys1,
    "osu_alltoall": dict_keys1,
    "osu_alltoallv": dict_keys1,
    "osu_barrier": dict_keys2,
    "osu_bcast": dict_keys1,
    "osu_bibw": dict_keys3,
    "osu_bw": dict_keys3,
    "osu_cas_latency": dict_keys4,
    "osu_fop_latency": dict_keys4,
    "osu_gather": dict_keys1,
    "osu_gatherv": dict_keys1,
    "osu_acc_latency": dict_keys4,
    "osu_get_bw": dict_keys4,
    "osu_get_latency": dict_keys1,
    "osu_iallgather": dict_keys1,
    "osu_iallgatherv": dict_keys1,
    "osu_ialltoall": dict_keys1,
    "osu_ialltoallv": dict_keys1,
    "osu_ialltoallw": dict_keys1,
    "osu_ibarrier": dict_keys2,
    "osu_ibcast": dict_keys1,
    "osu_igather": dict_keys1,
    "osu_igatherv": dict_keys1,
    "osu_iscatter": dict_keys1,
    "osu_iscatterv": dict_keys1,
    "osu_latency": dict_keys3,
    "osu_latency_mt": dict_keys5,
    "osu_multi_lat": dict_keys6,
    "osu_put_bibw": dict_keys4,
    "osu_put_bw": dict_keys4,
    "osu_put_latency": dict_keys4,
    "osu_reduce": dict_keys1,
    "osu_reduce_scatter": dict_keys1,
    "osu_scatter": dict_keys1,
    "osu_scatterv": dict_keys1,
}

def osu_parser(content):
    """parse and validate the yaml content and return the command"""
    name = content["name"]
    #print (name,dict_keys1, lookup_table[name])
    for key in lookup_table[name]:
        if key not in content:
            #print ("Key:" + key + " not in " + name)
            return None


    if dict_keys1 == lookup_table[name]:
        mpi_cmd = "mpirun -np " + str(content["proc"])  + " " + name \
              + " -m " + str(content["min_message_size"]) + ":" + str(content["max_message_size"]) \
              + " -i " + str(content["iter_msg_size"]) \
              + " -M " + str(content["max_mem_per_proc"]) \
              + " -x " + str(content["warmup_iter"]) \
              + " -t " + str(content["calls"])
        if content["full_format"] == True:
            mpi_cmd += " -f"
    elif dict_keys2 == lookup_table[name]:
        mpi_cmd = "mpirun -np " + str(content["proc"]) + " " + name \
                    +  " -i " + str(content["iter_msg_size"]) \
                    + " -x " + str(content["warmup_iter"]) \
                    + " -t " + str(content["calls"])
        if content["full_format"] == True:
            mpi_cmd += " -f"
    elif dict_keys3 == lookup_table[name]:
        mpi_cmd = "mpirun -np 2 " + name \
                + " -i " + str(content["iter"])  \
                + " -x " + str(content["warmup_iter"])
    elif dict_keys4 == lookup_table[name]:
        mpi_cmd = "mpirun -np 2 " + name \
                    + " -w " + str(content["win_option"]) \
                    + " -s " + str(content["sync_option"]) \
                    + " -i " + str(content["iter"]) \
                    + " -x " + str(content["warmup_iter"])
    elif dict_keys5 == lookup_table[name]:
        mpi_cmd = "mpirun -np 2 " + name \
                    + " -i " + str(content["iter"]) \
                    + " -x " + str(content["warmup_iter"]) \
                    + " -t " + str(content["threads"])
    elif dict_keys6 == lookup_table[name]:
        mpi_cmd = "mpirun -np " + str(content["proc"]) + " " + name \
                + " -i " + str(content["iter"]) \
                + " -x " + str(content["warmup_iter"])

    return mpi_cmd


def run_osu_microbenchmark(config):
    """run the OSU benchmark"""

    if config == None:
        config = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],
                              "buildtest",
                              "benchmark",
                              "osu.yaml")

    ext = os.path.splitext(config)[1]
    ext = ext[1:]

    if ext != "yaml":
        print("Invalid Extension: " + ext + " expecting extension .yaml")
        return

    print ("Reading Yaml file: " + config + "\n")
    fd=open(config,'r')
    content=yaml.safe_load(fd)
    print ("Loading YAML content \n")
    modulefile = content["benchmark"]["module"]
    num_tests = len(content["benchmark"]["test"])

    testlist = []

    print ("Parsing YAML content ...")
    for i in content["benchmark"]["test"]:
        mpi_cmd = osu_parser(i)
        if mpi_cmd == None:
            continue

        testname = "/tmp/" + i["name"] + ".sh"
        fd = open(testname,"w")
        fd.write("#!/bin/sh" + "\n")
        fd.write("module load " + modulefile +  "\n")
        fd.write(mpi_cmd)
        fd.close()
        os.chmod(testname, stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
        testlist.append(testname)
    print ("Tests Generation complete. All tests are written under /tmp/osu* \n")

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(config_opts["BUILDTEST_RUN_DIR"],runfile)

    fd = open(run_output_file,"w")
    write_system_info(fd)
    header = "{:-<45} START OF TEST {:-<45} \n".format("", "")
    fd.write(header)

    for test in testlist:
        name = os.path.splitext(os.path.basename(test))[0]
        print (name + "[ " + test + " ]         [RUNNING]" )
        ret = subprocess.Popen(test,shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        output = ret.communicate()[0]
        output=output.decode("utf-8")

        time.sleep(0.25)
        ret_code = ret.returncode
        if ret_code == 0:
            print (name + "[ " + test + " ]         [PASSED]" )
        else:
            print (name + "[ " + test + " ]         [FAILED]" )

        fd.write("Test Name:" + test + "\n")
        fd.write("Return Code: " + str(ret_code) + "\n")
        header = "{:-<45} START OF TEST OUTPUT {:-<45} \n".format("", "")
        footer = "{:-<45} END OF TEST OUTPUT {:-<45} \n".format("", "")
        fd.write(header)
        fd.write(output)
        fd.write(footer)

    print ("Writing Test Results to " + run_output_file)

def list_osu_tests():
    """List of tests in OSU MicroBenchmark."""

    print ("""
    -------------------- TEST BREAKDOWN ---------------------------------
    osu_bibw - Bidirectional Bandwidth Test
    osu_bw - Bandwidth Test
    osu_latency - Latency Test
    osu_put_latency - Latency Test for Put
    osu_get_latency - Latency Test for Get
    osu_put_bw - Bandwidth Test for Put
    osu_get_bw - Bandwidth Test for Get
    osu_put_bibw - Bidirectional Bandwidth Test for Put
    osu_acc_latency - Latency Test for Accumulate
    osu_cas_latency - Latency Test for Compare and Swap
    osu_fop_latency - Latency Test for Fetch and Op
    osu_allgather - MPI_Allgather Latency Test
    osu_allgatherv - MPI_Allgatherv Latency Test
    osu_allreduce - MPI_Allreduce Latency Test
    osu_alltoall - MPI_Alltoall Latency Test
    osu_alltoallv - MPI_Alltoallv Latency Test
    osu_bcast - MPI_Bcast Latency Test
    osu_gather - MPI_Gather Latency Test
    osu_gatherv - MPI_Gatherv Latency Test
    osu_reduce - MPI_Reduce Latency Test
    osu_reduce_scatter - MPI_Reduce_scatter Latency Test
    osu_scatter - MPI_Scatter Latency Test
    osu_scatterv - MPI_Scatterv Latency Test
    osu_iallgather - MPI_Iallgather Latency Test
    osu_iallreduce - MPI_Iallreduce Latency Test
    osu_ialltoall - MPI_Ialltoall Latency Test
    osu_ibcast - MPI_Ibcast Latency Test
    osu_igather - MPI_Igather Latency Test
    osu_ireduce - MPI_Iallreduce Latency Test
    osu_iscatter - MPI_Iscatter Latency Test
    -----------------------------------------------------------------

    ----------------- POINT-TO-POINT MPI BENCHMARKS -----------------
    osu_latency - Latency Test
    osu_latency_mt - Multi-threaded Latency Test
    osu_bw - Bandwidth Test
    osu_bibw - Bidirectional Bandwidth Test
    osu_mbw_mr - Multiple Bandwidth / Message Rate Test
    osu_multi_lat - Multi-pair Latency Test
    -----------------------------------------------------------------

    ---------------- COLLECTIVE MPI BENCHMARKS ----------------------
    osu_allgather - MPI_Allgather Latency Test
    osu_allgatherv - MPI_Allgatherv Latency Test
    osu_allreduce - MPI_Allreduce Latency Test
    osu_alltoall - MPI_Alltoall Latency Test
    osu_alltoallv - MPI_Alltoallv Latency Test
    osu_barrier - MPI_Barrier Latency Test
    osu_bcast - MPI_Bcast Latency Test
    osu_gather - MPI_Gather Latency Test
    osu_gatherv - MPI_Gatherv Latency Test
    osu_reduce - MPI_Reduce Latency Test
    osu_reduce_scatter - MPI_Reduce_scatter Latency Test
    osu_scatter - MPI_Scatter Latency Test
    osu_scatterv - MPI_Scatterv Latency Test
    -----------------------------------------------------------------

    ------------ NON-BLOCKING COLLECTIVE MPI BENCHMARKS -------------
    osu_iallgather - MPI_Iallgather Latency Test
    osu_iallgatherv - MPI_Iallgatherv Latency Test
    osu_iallreduce - MPI_Iallreduce Latency Test
    osu_ialltoall - MPI_Ialltoall Latency Test
    osu_ialltoallv - MPI_Ialltoallv Latency Test
    osu_ialltoallw - MPI_Ialltoallw Latency Test
    osu_ibarrier - MPI_Ibarrier Latency Test
    osu_ibcast - MPI_Ibcast Latency Test
    osu_igather - MPI_Igather Latency Test
    osu_igatherv - MPI_Igatherv Latency Test
    osu_ireduce - MPI_Ireduce Latency Test
    osu_iscatter - MPI_Iscatter Latency Test
    osu_iscatterv - MPI_Iscatterv Latency Test
    -----------------------------------------------------------------

    ------------------- ONE-SIDED MPI BENCHMARKS --------------------
    osu_put_latency - Latency Test for Put with Active/Passive Synchronization
    osu_get_latency - Latency Test for Get with Active/Passive Synchronization
    osu_put_bw - Bandwidth Test for Put with Active/Passive Synchronization
    osu_get_bw - Bandwidth Test for Get with Active/Passive Synchronization
    osu_put_bibw - Bi-directional Bandwidth Test for Put with Active Synchronization
    osu_acc_latency - Latency Test for Accumulate with Active/Passive Synchronization
    osu_cas_latency - Latency Test for Compare and Swap with Active/Passive Synchronization
    osu_fop_latency - Latency Test for Fetch and Op with Active/Passive Synchronization
    osu_get_acc_latency - Latency Test for Get_accumulate with Active/Passive Synchronization
   -----------------------------------------------------------------

    For more information please refer to http://mvapich.cse.ohio-state.edu/benchmarks/

    """)

def osu_info():
    """display yaml key description for OSU Benchmark"""

    print ("""
      Keys              |    Description
    --------------------+---------------------------------------------------------------------------------------------------------------
      proc              |    Number of MPI Processes
    --------------------+---------------------------------------------------------------------------------------------------------------
      min_message_size  |    set the minimum and/or the maximum message size to MIN and/or MAX bytes respectively
    --------------------+---------------------------------------------------------------------------------------------------------------
      max_message_size  |    set the minimum and/or the maximum message size to MIN and/or MAX bytes respectively
    --------------------+---------------------------------------------------------------------------------------------------------------
      max_mem_per_proc  |    set per process maximum memory consumption to SIZE bytes (default 536870912)
    --------------------+---------------------------------------------------------------------------------------------------------------
      iter_msg_size     |    set iterations per message size to ITER (default 1000 for small messages, 100 for large messages)
    --------------------+---------------------------------------------------------------------------------------------------------------
      warmup_iter       |    set number of warmup iterations to skip before timing (default 200)
    --------------------+---------------------------------------------------------------------------------------------------------------
      full_format       |    print full format listing (MIN/MAX latency and ITERATIONS displayed in addition to AVERAGE latency)
    --------------------+---------------------------------------------------------------------------------------------------------------
      calls             |    set the number of MPI_Test() calls during the dummy computation, set CALLS to 100, 1000, or any number > 0.
    --------------------+---------------------------------------------------------------------------------------------------------------
      iter              |    number of iterations for timing (default 100)
    --------------------+---------------------------------------------------------------------------------------------------------------
      win_option        |    <win_option> can be any of the follows:
                        |    create            use MPI_Win_create to create an MPI Window object
                        |    allocate          use MPI_Win_allocate to create an MPI Window object
                        |    dynamic           use MPI_Win_create_dynamic to create an MPI Window object
    --------------------+---------------------------------------------------------------------------------------------------------------
      sync_option       |    <sync_option> can be any of the follows:
                        |    pscw              use Post/Start/Complete/Wait synchronization calls
                        |    fence             use MPI_Win_fence synchronization call
                        |    lock              use MPI_Win_lock/unlock synchronizations calls
                        |    flush             use MPI_Win_flush synchronization call
                        |    flush_local       use MPI_Win_flush_local synchronization call
                        |    lock_all          use MPI_Win_lock_all/unlock_all synchronization calls
    --------------------+---------------------------------------------------------------------------------------------------------------
      threads           |    number of recv threads to test with (min: 1, default: 2, max: 128)
    --------------------+---------------------------------------------------------------------------------------------------------------
    """)
