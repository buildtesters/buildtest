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

`Summit <https://docs.olcf.ornl.gov/systems/summit_user_guide.html>`_ is a training
system for Summit at OLCF, which is using a IBM Load Sharing
Facility (LSF) as their batch scheduler. Ascent has two
queues **batch** and **test**. To declare LSF executors we define them under ``lsf``
section within the ``executors`` section.

The default batch configuration is defined in ``defaults``, for instance we set the fields ``pollinterval``, ``maxpendtime``
and to **30s** and **300s** each. The field ``account`` is used to specify project account where all jobs will be charged. This can be
customized to each site but and can be changed in the configuration file or overridden via command line ``buildtest build --account <ACCOUNT>``.


.. literalinclude:: ../../tests/settings/summit.yml
   :language: yaml
   :emphasize-lines: 19-23,37-39

Argonne National Laboratory
---------------------------

`Joint Laboratory for System Evaluation (JLSE) <https://www.jlse.anl.gov/>`_ provides
a testbed of emerging HPC systems, the default scheduler is Cobalt, this is
defined in the ``cobalt`` section defined in the executor field.

We set default launcher to qsub defined with ``launcher: qsub``. This is inherited
for all batch executors. In each cobalt executor the ``queue`` property will specify
the queue name to submit job, for instance the executor ``yarrow`` with ``queue: yarrow``
will submit job using ``qsub -q yarrow`` when using this executor.

.. literalinclude:: ../../tests/settings/jlse.yml
   :language: yaml