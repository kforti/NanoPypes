.. highlight:: shell

.. _quick_start:

===========
Quick-Start
===========


NanoPypes is a python package for managing and analysing ONT sequence data using distributed computing environments.

Installation Instructions:
--------------------------
You will need Albacore installed.
:ref:`install_albacore`:


Install from source
-------------------
NanoPypes Source:

.. code-block:: console

    $ git clone https://github.com/kforti/NanoPypes
    $ cd NanoPypes
    $ python3 setup.py install --user


Parallel basecalling with ONT's Albacore
-----------------------------------------
Run Albacore (replace all < > with their appropriate value):

.. code-block:: console

    $ run_pipeline --input_path <path/to/minion/sequence/data> --name albacore_basecaller --compute_name umass_ghpcc_lsf_basecall --kit <name> --flowcell <name>

run_pipeline options:

.. code-block:: yaml

    config  The path to the cluster configuration yaml ##<path/to/config>
    -i, --input_path   Path to the input data
    -pn, --pipeline_name   Name of the pipeline- Will be used to find the correct config file if no config path is given
    -pc, --pipeline_config   Path to a pipeline config file
    -cc, --compute_config   Path to a compute config file
    -cn, --compute_name   Path to a compute config file

    pipeline_args   Arguments that are required by the pipeline that is being run.
    ## The example above takes the following two arguments for the selected pipeline:
    -k --kit   The type of ONT kit used in the sequencing run. required=True
    -f --flowcell   The type of ONT kit used in the sequencing run. required=True



Pre-built yaml config files for pipelines and computational resources
------------------------------
A yaml file is used to pass compute resource and pipeline configuration information to NanoPypes. There are multiple clusters already in the config files that are installed with the package.
New configurations can be added to your nanopypes installation or you can provide a path to a custom compute and/or pipeline configuration file.

Below, is an example configuration for building a cluster ontop of LSF and its name is 'cluster1'.

.. code-block:: yaml

    computes:
        cluster1:
            cluster_type: lsf
            job_time: 04:00
            project: /project/umw_athma_pai
            queue: long
            workers_per_job: 2
            num_workers: 20
            worker_cores: 2
            worker_memory: 4096
            debug: True


yaml options::

    -cluster_type:  # The type of job scheduler on your HPC cluster ##currently supports LSF, Slurm and Kubernetes
    -job_time  # Number of physical cores per job (for cluster) ##BSUB -W
    -project  # The project space path on the cluster ##BSUB -p
    -queue  # The queue that the worker jobs should be submitted to ##BSUB -q
    -workers_per_job  # The number of workers per job
    -num_workers   # The total number of workers in the cluster
    -worker_cores: #The number of cores per worker
    -worker_memory:  # The amount of memory per worker
    -debug   # If true, the cluster will produce extra logging information

.. More information about :ref:`cluster_configuration`

A config file for your cluster will be saved to the save_path

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index
   installation

