NanoPypes
==========

NanoPypes is a python package for managing and analysing ONT sequence data using distributed computing environments.


.. py:currentmodule:: cli
.. autofunction:: albacore_basecaller

Quick-Start
===========

Install
------------
pip::

    pip install nanopypes

Parallel basecalling with ONT's Albacore- command line
-------------------------------------------------------
Single command- pass a config and/or individual parameters.::

    nanopypes_albacore_basecaller path/to/yaml/config

For a full list of parameters.::

    nanopypes_albacore_basecaller --help


Building the yaml config file.
------------------------------
Create a .yml file with the following parameters.::

  basecall:
      input_path:
      save_path:
      flowcell: FLO-MIN106
      kit: SQK-LSK109
      barcoding: False
      output_format: fast5
      worker_threads: 1
      recursive: False
      reads_per_fastq: 1000
      data_splits:
    compute:
        cluster1:
            job_time: 04:00
            mem: 2048
            ncpus: 10
            project:
            queue: short
            workers: 10
            cores: 10
            memory: 2 GB
            scale_value: 200
            cluster_type: LSF
    networking:
        network1:
            compute_name:
            address:
            password:
    pipe:
        name: None

Parallel basecalling with ONT's Albacore- pure python
-------------------------------------------------------
Set your configurations and create an instance of Albacore.::

    from nanopypes.tools import basecaller

    basecaller(config="path/to/yaml/config",
               data_splits=300,
               basecaller="albacore")


Create an instance of Cluster to connect to your compute resources.::

    compute = Cluster(config)

Execute the basecall function.::

    from nanopypes.pipes import AlbacoreBasecaller

    basecaller = AlbacoreBasecaller(albacore, compute, data_splits=300)
    basecalled_data = basecaller()


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   modules
   contributing
   authors
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
