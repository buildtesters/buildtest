Site Examples
==============

NERSC
-----

`NERSC <http://nersc.gov/>`_ provides High Performance Computing system to support research in the Office of Science program
offices. Currently, NERSC provides two HPC systems including `Perlmutter <https://docs.nersc.gov/systems/perlmutter/system_details/>`_ and
`Cori <https://docs.nersc.gov/systems/cori/>`_. In example below we see the configuration for Cori and Perlmutter. Note that we can define a
single configuration for both systems. Perlmutter is using `Lmod` while Cori is running `environment-modules`. We define Local executors and
Slurm executors for each system which are mapped to qos provided by our Slurm cluster.


.. rli:: https://github.com/buildtesters/buildtest-cori/blob/devel/config.yml
   :language: yaml

Ascent @ OLCF
---------------

`Ascent <https://docs.olcf.ornl.gov/systems/ascent_user_guide.html>`_ is a training
system for Summit at OLCF, which is using a IBM Load Sharing
Facility (LSF) as their batch scheduler. Ascent has two
queues **batch** and **test**. To declare LSF executors we define them under ``lsf``
section within the ``executors`` section.

The default launcher is `bsub` which can be defined under ``defaults``. The
``pollinterval`` will poll LSF jobs every 10 seconds using ``bjobs``. The
``pollinterval`` accepts a range between **10 - 300** seconds as defined in
schema. In order to avoid polling scheduler excessively pick a number that is best
suitable for your site

.. literalinclude:: ../../tests/settings/ascent.yml
   :language: yaml

JLSE @ ANL
-----------

`Joint Laboratory for System Evaluation (JLSE) <https://www.jlse.anl.gov/>`_ provides
a testbed of emerging HPC systems, the default scheduler is Cobalt, this is
defined in the ``cobalt`` section defined in the executor field.

We set default launcher to qsub defined with ``launcher: qsub``. This is inherited
for all batch executors. In each cobalt executor the ``queue`` property will specify
the queue name to submit job, for instance the executor ``yarrow`` with ``queue: yarrow``
will submit job using ``qsub -q yarrow`` when using this executor.

.. literalinclude:: ../../tests/settings/jlse.yml
   :language: yaml