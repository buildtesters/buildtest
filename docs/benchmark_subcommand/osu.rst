OSU MicroBenchmark
===================

OSU MicroBenchmark is a benchmark suite by Ohio State University that is commonly packaged
as part of mvapich2 software tool. The OSU MicroBenchmark is designed to test MPI
communication between process. For more information about this benchmark check out
http://mvapich.cse.ohio-state.edu/benchmarks/

.. program-output:: cat docgen/buildtest_benchmark_osu_-h.txt


To get a sense of all the test available from this benchmark supported by buildtest you
can run ``buildtest benchmark osu -l`` which will give a listing all of tests.

.. program-output:: cat docgen/buildtest_benchmark_osu_--list.txt



There is a YAML file for the OSU benchmark that can be found at  https://raw.githubusercontent.com/HPC-buildtest/buildtest-configs/master/buildtest/benchmark/osu.yaml.
This is the default configuration file that will be used, you may specify an alternative file using the `-c` option.

A description of all the yaml keys can be found by using the ``-i`` or ``--info`` option. Each of these options
correspond to a particular option found in the test suite.

.. program-output:: cat docgen/buildtest_benchmark_osu_--info.txt

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
