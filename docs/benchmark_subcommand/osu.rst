OSU MicroBenchmark
===================

OSU MicroBenchmark is a benchmark suite by Ohio State University that is commonly packaged
as part of mvapich2 software tool. The OSU MicroBenchmark is designed to test MPI
communication between process. For more information about this benchmark check out
http://mvapich.cse.ohio-state.edu/benchmarks/

::

    (siddis14-TgVBs13r) buildtest-framework[master !?] $ buildtest benchmark osu --help
    usage: buildtest [options] benchmark osu [-h] [-r] [-i] [-l] [-c CONFIG]

    optional arguments:
    -h, --help            show this help message and exit
    -r, --run             Run Benchmark
    -i, --info            show yaml key description
    -l, --list            List of tests available for OSU Benchmark
    -c CONFIG, --config CONFIG
                        OSU Yaml Configuration File



To get a sense of all the test available from this benchmark supported by buildtest you
can run `_buildtest benchmark osu -l` which will give a listing all of tests.

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest benchmark osu -l
    Check Configuration

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

    ------------------------- POINT-TO-POINT MPI BENCHMARKS -------------------------
    osu_latency - Latency Test
    osu_latency_mt - Multi-threaded Latency Test
    osu_bw - Bandwidth Test
    osu_bibw - Bidirectional Bandwidth Test
    osu_mbw_mr - Multiple Bandwidth / Message Rate Test
    osu_multi_lat - Multi-pair Latency Test
    -----------------------------------------------------------------------------

    ------------------------- COLLECTIVE MPI BENCHMARKS -------------------------
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
    -----------------------------------------------------------------------------

    ------------------ NON-BLOCKING COLLECTIVE MPI BENCHMARKS -------------------
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
    -----------------------------------------------------------------------------

    ------------------------- ONE-SIDED MPI BENCHMARKS -------------------------
    osu_put_latency - Latency Test for Put with Active/Passive Synchronization
    osu_get_latency - Latency Test for Get with Active/Passive Synchronization
    osu_put_bw - Bandwidth Test for Put with Active/Passive Synchronization
    osu_get_bw - Bandwidth Test for Get with Active/Passive Synchronization
    osu_put_bibw - Bi-directional Bandwidth Test for Put with Active Synchronization
    osu_acc_latency - Latency Test for Accumulate with Active/Passive Synchronization
    osu_cas_latency - Latency Test for Compare and Swap with Active/Passive Synchronization
    osu_fop_latency - Latency Test for Fetch and Op with Active/Passive Synchronization
    osu_get_acc_latency - Latency Test for Get_accumulate with Active/Passive Synchronization
    -----------------------------------------------------------------------------

    For more information please refer to http://mvapich.cse.ohio-state.edu/benchmarks/


There is a YAML file for the OSU benchmark that can be found at  https://raw.githubusercontent.com/HPC-buildtest/buildtest-configs/master/buildtest/benchmark/osu.yaml.
This is the default configuration file that will be used, you may specify an alternative file using the `-c` option.

A description of all the yaml keys can be found by using the ``-i`` or ``--info`` option. Each of these options
correspond to a particular option found in the test suite.

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest benchmark osu -i
    Check Configuration

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


To run the benchmark just specify the ``-r`` or ``--run`` option and it will run all the test and
return an output ``.run`` file with the results.


.. Note:: It will take a couple minutes to finish all of the tests. Please be patient!


::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest benchmark osu -r
    Check Configuration
    Reading Yaml file: /home/siddis14/github/buildtest-configs/buildtest/benchmark/osu.yaml

    Loading YAML content

    Parsing YAML content ...
    Tests Generation complete. All tests are written under /tmp/osu*

    osu_allgather[ /tmp/osu_allgather.sh ]         [RUNNING]
    osu_allgather[ /tmp/osu_allgather.sh ]         [PASSED]
    osu_allgatherv[ /tmp/osu_allgatherv.sh ]         [RUNNING]
    osu_allgatherv[ /tmp/osu_allgatherv.sh ]         [PASSED]
    osu_allreduce[ /tmp/osu_allreduce.sh ]         [RUNNING]
    osu_allreduce[ /tmp/osu_allreduce.sh ]         [PASSED]
    osu_alltoall[ /tmp/osu_alltoall.sh ]         [RUNNING]
    osu_alltoall[ /tmp/osu_alltoall.sh ]         [PASSED]
    osu_alltoallv[ /tmp/osu_alltoallv.sh ]         [RUNNING]
    osu_alltoallv[ /tmp/osu_alltoallv.sh ]         [PASSED]
    osu_barrier[ /tmp/osu_barrier.sh ]         [RUNNING]
    osu_barrier[ /tmp/osu_barrier.sh ]         [PASSED]
    osu_bcast[ /tmp/osu_bcast.sh ]         [RUNNING]
    osu_bcast[ /tmp/osu_bcast.sh ]         [PASSED]
    osu_bibw[ /tmp/osu_bibw.sh ]         [RUNNING]
    osu_bibw[ /tmp/osu_bibw.sh ]         [PASSED]
    osu_bw[ /tmp/osu_bw.sh ]         [RUNNING]
    osu_bw[ /tmp/osu_bw.sh ]         [PASSED]
    osu_cas_latency[ /tmp/osu_cas_latency.sh ]         [RUNNING]
    osu_cas_latency[ /tmp/osu_cas_latency.sh ]         [PASSED]
    osu_fop_latency[ /tmp/osu_fop_latency.sh ]         [RUNNING]
    osu_fop_latency[ /tmp/osu_fop_latency.sh ]         [PASSED]
    osu_gather[ /tmp/osu_gather.sh ]         [RUNNING]
    osu_gather[ /tmp/osu_gather.sh ]         [PASSED]
    osu_gatherv[ /tmp/osu_gatherv.sh ]         [RUNNING]
    osu_gatherv[ /tmp/osu_gatherv.sh ]         [PASSED]
    osu_acc_latency[ /tmp/osu_acc_latency.sh ]         [RUNNING]
    osu_acc_latency[ /tmp/osu_acc_latency.sh ]         [PASSED]
    osu_get_bw[ /tmp/osu_get_bw.sh ]         [RUNNING]
    osu_get_bw[ /tmp/osu_get_bw.sh ]         [PASSED]
    osu_iallgather[ /tmp/osu_iallgather.sh ]         [RUNNING]
    osu_iallgather[ /tmp/osu_iallgather.sh ]         [PASSED]
    osu_iallgatherv[ /tmp/osu_iallgatherv.sh ]         [RUNNING]
    osu_iallgatherv[ /tmp/osu_iallgatherv.sh ]         [PASSED]
    osu_ialltoall[ /tmp/osu_ialltoall.sh ]         [RUNNING]
    osu_ialltoall[ /tmp/osu_ialltoall.sh ]         [PASSED]
    osu_ialltoallv[ /tmp/osu_ialltoallv.sh ]         [RUNNING]
    osu_ialltoallv[ /tmp/osu_ialltoallv.sh ]         [PASSED]
    osu_ialltoallw[ /tmp/osu_ialltoallw.sh ]         [RUNNING]
    osu_ialltoallw[ /tmp/osu_ialltoallw.sh ]         [PASSED]
    osu_ibarrier[ /tmp/osu_ibarrier.sh ]         [RUNNING]
    osu_ibarrier[ /tmp/osu_ibarrier.sh ]         [PASSED]
    osu_ibcast[ /tmp/osu_ibcast.sh ]         [RUNNING]
    osu_ibcast[ /tmp/osu_ibcast.sh ]         [PASSED]
    osu_igather[ /tmp/osu_igather.sh ]         [RUNNING]
    osu_igather[ /tmp/osu_igather.sh ]         [PASSED]
    osu_igatherv[ /tmp/osu_igatherv.sh ]         [RUNNING]
    osu_igatherv[ /tmp/osu_igatherv.sh ]         [PASSED]
    osu_iscatter[ /tmp/osu_iscatter.sh ]         [RUNNING]
    osu_iscatter[ /tmp/osu_iscatter.sh ]         [PASSED]
    osu_iscatterv[ /tmp/osu_iscatterv.sh ]         [RUNNING]
    osu_iscatterv[ /tmp/osu_iscatterv.sh ]         [PASSED]
    osu_latency[ /tmp/osu_latency.sh ]         [RUNNING]
    osu_latency[ /tmp/osu_latency.sh ]         [PASSED]
    osu_latency_mt[ /tmp/osu_latency_mt.sh ]         [RUNNING]
    osu_latency_mt[ /tmp/osu_latency_mt.sh ]         [PASSED]
    osu_multi_lat[ /tmp/osu_multi_lat.sh ]         [RUNNING]
    osu_multi_lat[ /tmp/osu_multi_lat.sh ]         [PASSED]
    osu_put_bibw[ /tmp/osu_put_bibw.sh ]         [RUNNING]
    osu_put_bibw[ /tmp/osu_put_bibw.sh ]         [PASSED]
    osu_put_bw[ /tmp/osu_put_bw.sh ]         [RUNNING]
    osu_put_bw[ /tmp/osu_put_bw.sh ]         [PASSED]
    osu_put_latency[ /tmp/osu_put_latency.sh ]         [RUNNING]
    osu_put_latency[ /tmp/osu_put_latency.sh ]         [PASSED]
    osu_reduce[ /tmp/osu_reduce.sh ]         [RUNNING]
    osu_reduce[ /tmp/osu_reduce.sh ]         [PASSED]
    osu_reduce_scatter[ /tmp/osu_reduce_scatter.sh ]         [RUNNING]
    osu_reduce_scatter[ /tmp/osu_reduce_scatter.sh ]         [PASSED]
    osu_scatter[ /tmp/osu_scatter.sh ]         [RUNNING]
    osu_scatter[ /tmp/osu_scatter.sh ]         [PASSED]
    osu_scatterv[ /tmp/osu_scatterv.sh ]         [RUNNING]
    osu_scatterv[ /tmp/osu_scatterv.sh ]         [PASSED]
    Writing Test Results to /tmp/buildtest_16_53_25_01_2019.run
