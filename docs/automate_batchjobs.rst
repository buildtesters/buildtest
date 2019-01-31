Automate Batch Job submission (``buildtest --submitjob``)
============================================================

buildtest can even automate batch job submission once you have created the
jobscripts via buildtest. To do this you need to use ``buildtest --submitjob``
flag.

**--submitjob** will take a directory or file to your job script. If it is a
file, then it will submit the job to scheduler, in the case of a directory, it
will submit all jobscripts in the particular directory to the scheduler.

Job Submission by File
----------------------

::

   [siddis14@amrndhl1228 buildtest-framework]$  buildtest --submitjob /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/Algorithm/diff.lsf
   Job <2531> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/Algorithm/diff.lsf  to scheduler

Job Submission by Directory
---------------------------

::

   [siddis14@amrndhl1228 buildtest-framework]$ buildtest --submitjob /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/
   Job <2532> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/perl_-v.lsf  to scheduler
   Job <2533> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/hello.pl.lsf  to scheduler
   Job <2534> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/Algorithm/diff.lsf  to scheduler
   Job <2535> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AnyData/AnyData.lsf  to scheduler
   Job <2536> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/Authen/SASL.lsf  to scheduler
   Job <2537> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/Args.lsf  to scheduler
   Job <2538> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/State.lsf  to scheduler
   Job <2539> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/File.lsf  to scheduler
   Job <2540> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/Std.lsf  to scheduler
   Job <2541> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/GetOpt.lsf  to scheduler
   Job <2542> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/Sys.lsf  to scheduler
   Job <2543> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/AppConfig.lsf  to scheduler
   Job <2544> is submitted to queue <short>.
   Submitting Job: /lustre/workspace/home/siddis14/buildtest-framework/testing/ebapp/Perl/5.22.1/foss/.2016.03/AppConfig/CGI.lsf  to scheduler



.. Note:: Use this option with care, as it may cause significant spike in workload.
