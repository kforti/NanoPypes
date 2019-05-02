NanoPypes
==========

NanoPypes is a python package for managing and analysing ONT sequence data using distributed computing environments.


Quick-Start
===========

Installation Instructions:
--------------------------
First, Albacore must be installed on your system, which requires a license from Oxford Nanopore Technologies. If you’ve purchased a Nanopore sequencing device from ONT then you already have this license.\n

To install Albacore on your system, login to the ONT Community Portal and go the the downloads page: https://community.nanoporetech.com/downloads. The Albacore downloads are under Archived Software.\n

Nanopypes has only been tested on Mac and Linux. Download either the Mac software or Linux software for python 3.5 or above. This will download a .whl package that you can install with the following command from the directory containing the .whl::

    pip3 install --user <name_of_albacore_package.whl>

** Replace <name_of_albacore_package.whl> with the name of the downloaded .whl package. The --user command is necessary if you do not have sudo access.

Next, make sure that the albacore executable is properly added to your PATH. The name of the executable is::

    read_fast5_basecaller.py

It is likely located in::

    ~/.local/bin/.


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

albacore_basecaller options:

    -n --cluster-name   The name of the cluster- located directly under computes in the config file. required=True
    -s --save-path   An empty save location for the basecalled data- if the directory does not exist it will be created but the parent directory must exist required=True
    -i --input-path   The path to a directory that contains batches of raw sequening data- likely titled pass. required=True
    -k --kit   The type of ONT kit used in the sequencing run. required=True
    -f --flowcell   The type of ONT kit used in the sequencing run. required=True
    -o --output-format   fastq or fast5 output format. required=True
    config  yaml config file for building the cluster

Building the yaml config file
------------------------------
Create a .yml file with the following parameters.:

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
Be aware of while selecting the number of channels to not overwhelm the data source/destination.:

    default -nchannels == 4

Running parallel_rsync.:

    parallel_rsync --nchannels <default=4> --local-path <path> --remote-path <path> --password <password> --direction <push or pull> --options <rsync options default='-vcr'>

parallel_rsync options:

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
