NanoPypes
==========

NanoPypes is a python package for managing and analysing ONT sequence data using distributed computing environments.


Quick-Start
===========

Install
------------
pip.::

    pip install nanopypes


Parallel basecalling with ONT's Albacore- pure python
-------------------------------------------------------
Create an instance of Albacore.::

    from nanopypes.albacore import *

    config = "path/to/yaml/config"
    albacore = Albacore(config)

Create an instance of Cluster to connect to your compute resources.::

    cluster = Cluster(config)

Execute the basecall function.::

    from nanopypes.nanopypes import basecall

    basecall(albacore, cluster)

Parallel basecalling with ONT's Albacore- command line
-------------------------------------------------------
Single command- pass a config and/or individual parameters.::

    parallel_basecaller path/to/yaml/config

For a full list of parameters.::

    parallel_basecaller --help


Building the yaml config file.
------------------------------
Create a .yml file with the following parameters.::

    basecall_config:
        input_path: path/to/raw/minion/data
        save_path: path/to/basecall/output
        flowcell: FLO-MIN106 # Flow cell used in sequencing run
        kit: SQK-LSK109 # Kit used in sequencing run
        barcoding: False
        output_format: fast5
        worker_threads: 1 # Albacore worker_threads- best to keep at 1
        recursive: False # all data will be non-recursive when Albacore is called
        reads_per_fastq: 1000
        cluster:
            job_time: 06:00  # May need optimizing based on number of reads
            mem: 40000 # Should be scaled with ncpus, workers and cores
            ncpus: 20 #1 worker per cpu
            project: /path/to/project/on/cluster
            queue: long
            workers: 20
            cores: 20
            memory: 40 GB
            scale_value: 100  # 100 scale_value / 20 cpus = 5 jobs
            cluster_type: LSF



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
