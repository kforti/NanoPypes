# -*- coding: utf-8 -*-
"""Console script for pai-nanopypes."""
import shutil
import os

import click

from nanopypes.run_pipes import albacore_basecaller as albacore
from nanopypes.run_pipes import ParallelRsync as prsync
from nanopypes.run_pipes import parallel_minimap2 as pmmap2
from nanopypes.config import Configuration
from nanopypes.compute import Cluster

from distributed import LocalCluster, Client



@click.command()
@click.option('-C', '--cluster-type', 'cluster_type', help='The type of cluster you plan to use for your analysis. ["lsf", "local]', required=True, type=str)
@click.option('-s', '--save-path', 'save_path', help='The number of batches to process at one time.', type=str)
def get_config_template(save_path, cluster_type):
    cluster_type = cluster_type.lower()
    template_name = "{}_albacore_template.yml".format(cluster_type)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    template_path = current_dir.replace("/nanopypes", ("/config_templates/" + template_name))

    shutil.copy(template_path, save_path)
    print("saved template to " + save_path)
    return 0


# @click.command()
# @click.option('-c', '--cluster-name', 'cluster_name', required=True, help="The cluster name in the config file- listed directly under computes.")
# @click.argument('config', required=True)
# def build_cluster(config, cluster_name):
#     config = Configuration(config)
#     compute_config = config.get_compute(cluster_name)
#     compute = Cluster(compute_config)
#     scheduler_address = compute.connect()
#     return scheduler_address
#

#############################################
## Run Pipes
#############################################

@click.command()
@click.option('-n', '--cluster-name', 'cluster_name', help='The name of the cluster- located directly under computes in the config file.', required=True, type=str)
@click.option('-s', '--save-path', 'save_path', help='An empty save location for the basecalled data- if the directory does not exist it will be created but the parent directory must exist', required=True, type=str)
@click.option('-i', '--input-path', 'input_path', help="The path to a directory that contains batches of raw sequening data- likely titled pass.", required=True, type=str)
@click.option('-k', '--kit', 'kit', help="The type of ONT kit used in the sequencing run.", required=True, type=str)
@click.option('-f', '--flowcell', 'flowcell', help="The type of ONT kit used in the sequencing run.", required=True, type=str)
@click.option('-o', '--output-format', 'output_format', help="fastq or fast5 output format.", required=True, type=str)
@click.argument('config', required=True)
def albacore_basecaller(config, cluster_name, kit, flowcell, input_path, save_path, output_format):
    """Console script for running the albacore parallel basecaller.
    :param cluster_name: The name of the cluster defined in the config yaml.
    :param kit: The name of the ONT kit used in the sequencing run."""
    #run_pipes function albacore_basecaller()
    config = Configuration(config)
    compute_config = config.get_compute(cluster_name)
    cluster = Cluster(compute_config)
    scheduler_address = cluster.connect()

    client = Client(scheduler_address)
    num_workers = cluster.expected_workers

    bc_data = albacore(kit=kit,
                       flowcell=flowcell,
                       input_path=input_path,
                       save_path=save_path,
                       output_format=output_format,
                       expected_workers=num_workers,
                       client=client
                       )
    return 0


@click.command()
@click.option('-n', '--nchannels', 'nchannels', help='The number of parallel rsync channels.', required=False, type=int)
@click.option('-l', '--local-path', 'local_path', help='The path to the data on your local machine.', required=True, type=str)
@click.option('-r', '--remote-path', 'remote_path', help='The path to where your data should be saved remotely, must include username', required=True, type=str)
@click.option('-p', '--password', 'password', help='HPC password', required=True, type=str)
@click.option('-d', '--direction', 'direction', help='Use "push" for local to remote. Use "pull" for remote to local. Default is set to push.', required=False, type=str)
@click.option('-o', '--options', 'rsync_options', help='a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr', required=False, type=str)
def parallel_rsync(local_path, remote_path, password, nchannels=4, rsync_options='-vcr', direction='push'):
    cluster = LocalCluster()
    client = Client(cluster)
    prsync(nchannels=nchannels, local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction,  client=client)
    return 0


@click.command()
@click.option('-n', '--cluster-name', 'cluster_name', help='The name of the cluster- located directly under computes in the config file.', required=True, type=str)
@click.option('-i', '--input-path', 'data_path', help='The path to a directory containing multiple fastq files.', required=True, type=str)
@click.option('-s', '--save-path', 'save_path', help='The path to where the output should be saved', required=True, type=str)
@click.option('-r', '--reference', 'reference', help='The path to your fasta reference file', required=True, type=str)
@click.option('-c', '--command', 'command', help='The minimap2 command that you would like to use. ["splice", "genomic", "rna", "overlap"]', required=True, type=str)
@click.argument('config', required=True)
def parallel_minimap2(config, cluster_name, input_path, reference, save_path, command):
    config = Configuration(config)
    compute_config = config.get_compute(cluster_name)
    compute = Cluster(compute_config)
    scheduler_address = compute.connect()

    client = Client(scheduler_address)
    pmmap2(input_path=input_path, reference=reference, save_path=save_path, command=command, client=client)
    return 0

