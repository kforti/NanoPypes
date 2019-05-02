NanoPypes
==========

NanoPypes is a python package for managing and analysing ONT sequence data using distributed computing environments.


Quick-Start
===========

Installation Instructions:
--------------------------
Install Albacore :ref:`install_albacore`:


Install From Source
-------------------
::

    git clone https://github.com/kforti/NanoPypes
    cd NanoPypes
    python3 setup.py install --user


Parallel basecalling with ONT's Albacore- command line
-------------------------------------------------------
::

    albacore_basecaller path/to/yaml/config --kit <name> --flowcell <name> --cluster-name <name>
    --save-path <path> --input-path <path > --output_format <fastq or fast5>

albacore_basecaller options::

    -n --cluster-name   The name of the cluster- located directly under computes in the config file. required=True
    -s --save-path   An empty save location for the basecalled data- if the directory does not exist it will be created but the parent directory must exist required=True
    -i --input-path   The path to a directory that contains batches of raw sequening data- likely titled pass. required=True
    -k --kit   The type of ONT kit used in the sequencing run. required=True
    -f --flowcell   The type of ONT kit used in the sequencing run. required=True
    -o --output-format   fastq or fast5 output format. required=True
    config  yaml config file for building the cluster

Building the yaml config file
------------------------------
Create a .yml file with the following parameters.::

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

Move your data with parallel rsync
------------------------------------
Be aware of while selecting the number of channels to not overwhelm the data source/destination.::

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
