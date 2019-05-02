=========
NanoPypes
=========


.. image:: https://img.shields.io/pypi/v/nanopypes.svg
        :target: https://pypi.python.org/pypi/nanopypes

.. image:: https://img.shields.io/travis/kforti/nanopypes.svg
        :target: https://travis-ci.org/kforti/nanopypes

.. image:: https://readthedocs.org/projects/nanopypes/badge/?version=latest
        :target: https://nanopypes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Package for rapidly building ONT MinIon sequence analysis pipelines


* Free software: GNU General Public License v3
* Documentation: https://nanopypes.readthedocs.io.


***Coming soon***
* parallel_variant_calling -> with samtools and bcftools
* guppy_cpu
* guppy_gpu
* kubernettes cluster support
* Slurm cluster support

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
Run Albacore (replace all < > with their appropriate value):

.. code-block:: console

    $ albacore_basecaller path/to/yaml/config --kit <name> --flowcell <name> --cluster-name <name>
    --save-path <path> --input-path <path > --output_format <fastq or fast5>

albacore_basecaller options:

.. code-block:: yaml

    config  The path to the cluster configuration yaml ##<path/to/config>
    -n --cluster-name   The name of the cluster- located directly under computes in the config file. required=True
    -s --save-path   An empty save location for the basecalled data- if the directory does not exist it will be created but the parent directory must exist required=True
    -i --input-path   The path to a directory that contains batches of raw sequening data- likely titled pass. required=True
    -k --kit   The type of ONT kit used in the sequencing run. required=True
    -f --flowcell   The type of ONT kit used in the sequencing run. required=True
    -o --output-format   fastq or fast5 output format. required=True



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


.. More information about :ref:`cluster_configuration`

NanoPypes comes with a pre-made config file for running albacore on an LSF cluster. You only need to add your project path to the file.

Build a config file:

.. code-block:: console

    $ get_config_template --save-path <path> --cluster-type <name>

A config file for your cluster will be saved to the save_path


Full Documentation
* Documentation: https://nanopypes.readthedocs.io.
