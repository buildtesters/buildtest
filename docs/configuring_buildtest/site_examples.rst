Site Examples
==============

NERSC
-----

`NERSC <http://nersc.gov/>`_ provides High Performance Computing system to support research in the Office of Science program
offices. NERSC has one production HPC systems `Perlmutter <https://docs.nersc.gov/systems/perlmutter/architecture/>`_ and
`muller` which is Test system for Perlmutter.

Shown below is the buildtest configuration at NERSC. We have defined multiple slurm executors, along with settings for
configuring compilers that is available on Perlmutter.

.. rli:: https://raw.githubusercontent.com/buildtesters/buildtest-nersc/devel/config.yml
   :language: yaml

Oak Ridge National Laboratory
-----------------------------

`Summit <https://docs.olcf.ornl.gov/systems/summit_user_guide.html>`_ is a IBM based system
hosted at Oak Ridge Leadership Computing Facility (OLCF). The system uses IBM Load Sharing
Facility (LSF) as their batch scheduler.

The ``system`` keyword is used to define the name of system which in this example is named ``summit``. The
``hostnames`` is used to specify a list of hostnames where buildtest can run in order to use this system configuration.

The system comes with several queues, for the purposes of this example we define 3 executors
that map to queues **batch** , **test** and **storage**. To declare LSF executors we define them under ``lsf``
section within the ``executors`` section.

The default batch configuration is defined in ``defaults``, for instance we set the fields ``pollinterval``, ``maxpendtime``
and to **30s** and **300s** each. The field ``account`` is used to specify project account where all jobs will be charged. This can be
customized to each site but and can be changed in the configuration file or overridden via command line ``buildtest build --account <ACCOUNT>``.

.. literalinclude:: ../../tests/settings/summit.yml
   :language: yaml
   :emphasize-lines: 2-5,19-23,37-43
