.. highlight:: shell

.. _quick_start:

===========
Quick-Start
===========


NanoPypes
==========

NanoPypes is a python package for managing and analysing ONT sequence data using distributed computing environments.


Quick-Start
===========

Installation Instructions:
--------------------------
You will need Albacore installed.
:ref:`install_albacore`:


Install From Source
-------------------
Source:

.. code-block:: console

    $ git clone https://github.com/kforti/NanoPypes
    $ cd NanoPypes
    $ python3 setup.py install --user


Parallel basecalling with ONT's Albacore- command line
-------------------------------------------------------
Run Albacore:

.. code-block:: console

    $ albacore_basecaller path/to/yaml/config --kit <name> --flowcell <name> --cluster-name <name>
    --save-path <path> --input-path <path > --output_format <fastq or fast5>

albacore_basecaller options:

.. code-block:: yaml

    -n --cluster-name   The name of the cluster- located directly under computes in the config file. required=True
    -s --save-path   An empty save location for the basecalled data- if the directory does not exist it will be created but the parent directory must exist required=True
    -i --input-path   The path to a directory that contains batches of raw sequening data- likely titled pass. required=True
    -k --kit   The type of ONT kit used in the sequencing run. required=True
    -f --flowcell   The type of ONT kit used in the sequencing run. required=True
    -o --output-format   fastq or fast5 output format. required=True
    config  yaml config file for building the cluster

Building the yaml config file
------------------------------
A yaml file is used to pass cluster configuration information to NanoPypes. Multiple clusters can be described.
In the example below, there is one cluster listed and its name is 'cluster1'.

The .yml file should have the following parameters.

.. code-block:: yaml

    computes:
        cluster1:
            job_time: 04:00
            mem: 2048
            umassmem: 2048
            ncpus: 10
            project: /path/to/project/space
            queue: short
            workers: 10
            cores: 10
            memory: 2 GB
            scale_value: 200
            cluster_type: LSF


yaml options::

    -job_time  #Number of physical cores per job (for cluster) ##BSUB -W
    -mem  #The amount of memory in bytes required by each job ##BSUM -M
    -umassmem: #Should be None if not using Umass LSF cluster. Memory described as - rusage[mem=umassmem] ##BSUB -R 'rusage[mem=2048]'
    -ncpus  #The number of physical cores per job ##BSUB -n
    -project  #The project space path on the cluster ##BSUB -p
    -queue  #The queue that the worker jobs should be submitted to ##BSUB -q
    -workers  #The number of workers per job
    -cores: #The number of cores per worker ##cores * workers == ncpus
    -memory:  # The amount of memory per worker ##memory *workers == mem
    -scale_value:  #The total number of workers that you would like in your cluster ## scale_value / workers == total number of jobs to be created
    -cluster_type:  #The type of job scheduler on your HPC cluster ##currently only supports LSF


More information about :ref:`cluster_configuration`


Move your data with parallel rsync
------------------------------------
Be aware while selecting the number of channels to not overwhelm the data source/destination.::

    default -nchannels == 4

Running parallel_rsync.::

    parallel_rsync --nchannels <default=4> --local-path <path> --remote-path <path> --password <password> --direction <push or pull> --options <rsync options default='-vcr'>

parallel_rsync options::

    -n --nchannels  The number of parallel rsync channels.
    -l --local-path  The path to the data on your local machine.
    -r --remote-path  The path to where your data should be saved remotely, must include username.
    -p --password  Remote location password
    -d --direction  Use "push" for local to remote. Use "pull" for remote to local. Default is set to push.
    -o --options  a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr



Parallel Read Mapping with Minimap2
-----------------------------------
Run Minimap2:

.. code-block:: console

    $ parallel_minimap2 <path/to/config> --command <name> --cluster-name <name> --input-path <path> --reference <path> --save-path <path>

Parallel minimap2 options::

    config
    -n --cluster-name  The name of the cluster- located directly under computes in the config file.
    -i --input-path  The path to a directory containing multiple fastq files.
    -s --save-path  The path to where the output should be saved.
    -r --reference  The path to your fasta reference file.
    -c --command  The minimap2 command that you would like to use. ["splice", "genomic", "rna", "overlap"]


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
