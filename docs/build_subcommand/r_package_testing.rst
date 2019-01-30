Building Tests for R packages (``buildtest build --r-package <R-PACKAGE>``)
===============================================================================

buildtest comes with option to build test for R packages to test R packages
are working as expected. The R tests are coming from the repository
https://github.com/HPC-buildtest/R-buildtest-config

In buildtest this repository is defined by variable ``BUILDTEST_R_REPO`` that
can be tweaked by environment variable or configuration file (``settings.yaml``)

buildtest supports tab completion for option ``--r-package`` which will show
a list of r packages available for testing.

To illustrate the tab completion feature see command below

.. code::

    [siddis14@prometheus buildtest-framework]$ buildtest build --r-package
    Display all 108 possibilities? (y or n)
    abc             animation       bigmemory       calibrate       evaluate        ffbase          forecast        gam             stringi         TeachingDemos   TraMineR
    abind           ape             bio3d           car             expm            fields          foreign         gamlss.data     stringr         tensor          tree
    acepack         arm             bit             caret           extrafont       filehash        formatR         gamlss.dist     strucchange     tensorA         trimcluster
    adabag          assertthat      bitops          caTools         FactoMineR      flashClust      Formula         gbm             subplex         testthat        tripack
    ade4            AUC             bnlearn         cgdsr           fail            flexclust       fossil          gclus           SuperLearner    TH.data         tseries
    adegenet        backports       boot            checkmate       fastcluster     flexmix         fpc             gdalUtils       SuppDists       tibble          tseriesChaos
    adephylo        base            bootstrap       chron           fastICA         fma             fpp             gdata           survival        tidyr           TTR
    ADGofTest       base64          brglm           cluster         fastmatch       FME             fracdiff        geepack         survivalROC     timeDate        unbalanced
    akima           BatchJobs       Brobdingnag     EasyABC         fdrtool         FNN             futile.logger   geiger          taxize          tkrplot
    AlgDesign       beanplot        Cairo           ellipse         ff              foreach         futile.options  statmod         tcltk           tm



To build r package test you must specify a ``R`` module. buildtest will
generate the binarytest along with any test from R package specified by
option ``--r-package``.

The following command ``buildtest build -s R/3.4.3-intel-2018a-X11-20171023 --r-package abc``
will build R test along with R package ``abc``

.. program-output:: cat scripts/r_packagetest_abc.txt


This option is compatible with ``--shell``, ``--enable-job`` and  ``--job-template`` if you want to build
tests with different shell or create job scripts
