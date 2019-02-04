Benchmark Subcommand
______________________


.. toctree::
   :titlesonly:
   :maxdepth: 1
   :glob:

   benchmark_subcommand/*


The benchmark submenu is further broken down into another sub-menu (one per benchmark). Currently,
buildtest supports OSU benchmark.

::

    (siddis14-TgVBs13r) buildtest-framework[master !?] $ buildtest benchmark --help
    usage: buildtest [options] benchmark [-h] {osu,hpl,hpcg} ...

    positional arguments:
      {osu,hpl,hpcg}  subcommand help
        osu           OSU MicroBenchmark sub menu
        hpl           High Performance Linpack sub menu
        hpcg          High Performance Conjugate Gradient sub menu

    optional arguments:
      -h, --help      show this help message and exit
