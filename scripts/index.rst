
Move your data with parallel rsync
------------------------------------
Be aware while selecting the number of channels to not overwhelm the data source/destination.::

    default -nchannels == 4

Run parallel_rsync (replace all < > with their appropriate value).:

.. code-block:: console

    $ parallel_rsync --nchannels <default=4> --local-path <path> --remote-path <path> --password <password> --direction <push or pull> --options <rsync options default='-vcr'>

parallel_rsync options::

    -n --nchannels  The number of parallel rsync channels.
    -l --local-path  The path to the data on your local machine.
    -r --remote-path  The path to where your data should be saved remotely, must include username.
    -p --password  Remote location password
    -d --direction  Use "push" for local to remote. Use "pull" for remote to local. Default is set to push.
    -o --options  a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr



Parallel Read Mapping with Minimap2
-----------------------------------
Run Minimap2 (replace all < > with their appropriate value):

.. code-block:: console

    $ parallel_minimap2 <path/to/config> --command <name> --cluster-name <name> --input-path <path> --reference <path> --save-path <path>

Parallel minimap2 options::

    config  The path to the cluster configuration yaml ##<path/to/config>
    -n --cluster-name  The name of the cluster- located directly under computes in the config file.
    -i --input-path  The path to a directory containing multiple fastq files.
    -s --save-path  The path to where the output should be saved.
    -r --reference  The path to your fasta reference file.
    -c --command  The minimap2 command that you would like to use. ["splice", "genomic", "rna", "overlap"]

