# -*- coding: utf-8 -*-
"""Console script for pai-nanopypes."""
import shutil
import os

import click

from nanopypes.run_pipes import albacore_basecaller as albacore
from nanopypes.run_pipes import ParallelRsync as prsync
from nanopypes.config import Configuration
from nanopypes.compute import Cluster

from distributed import LocalCluster, Client



@click.command()
@click.option('-C', '--cluster-type', 'cluster_type', help='The type of cluster you plan to use for your analysis. ["lsf", "local]', required=True, type=str)
@click.option('-s', '--save-path', 'save_path', help='The number of batches to process at one time.', type=str)
@click.option('-b', '--basecaller', 'basecaller', help='The basecaller you plan to use. ["albacore", "guppy-cpu", "guppy-gpu"]', type=str)
def get_config_template(save_path, cluster_type, basecaller):
    template_name = "{}_{}_template.yml".format(cluster_type, basecaller)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    template_path = current_dir.replace("/nanopypes", ("/config_templates/" + template_name))

    shutil.copy(template_path, save_path)
    print("saved template to " + save_path)
    return 0


@click.command()
@click.options('-c', '--cluster-name', 'cluster_name', required=True, help="The cluster name in the config file- listed directly under computes.")
@click.argument('config', required=True, help="Config file is required to build a cluster.")
def build_cluster(config, cluster_name):
    config = Configuration(config)
    compute_config = config.get_compute(cluster_name)
    compute = Cluster(compute_config)
    scheduler_address = compute.connect()
    print(scheduler_address)
    return scheduler_address


#############################################
## Run Pipes
#############################################

@click.command()
@click.option('-s', '--save-path', 'save_path', help='The save location for the basecalled data', required=False, type=str)
@click.option('-i', '--input-path', 'input_path', help="The type of ont kit used.", required=False, type=str)
@click.option('-k', '--kit', 'kit', help="The type of ont kit used.", required=False, type=str)
@click.option('-f', '--flowcell', 'flowcell', help="The type of ont flowcell used.", required=False, type=str)
@click.option('-o', '--output-format', 'output_format', help="fastq or fast5 output format.", required=False, type=str)
@click.argument('scheduler_address', required=True, help="A scheduler address can be obtained with the build_cluster command.")
def albacore_basecaller(scheduler_address, num_workers, kit, flowcell, input_path, save_path, output_format):
    """Console script for running the albacore parallel basecaller."""
    #run_pipes function albacore_basecaller()
    bc_data = albacore(kit=kit,
                       flowcell=flowcell,
                       input_path=input_path,
                       save_path=save_path,
                       output_format=output_format,
                       expected_workers=num_workers
                       )
    return 0


@click.command()
@click.option('-n', '--nchannels', 'nchannels', help='The number of parallel rsync channels.', required=True, type=int)
@click.option('-l', '--local-path', 'local_path', help='The path to the data on your local machine.', required=True, type=str)
@click.option('-r', '--remote-path', 'remote_path', help='The path to where your data should be saved remotely, must include username', required=True, type=str)
@click.option('-p', '--password', 'password', help='HPC password', required=True, type=str)
@click.option('-d', '--direction', 'direction', help='Use "push" for local to remote. Use "pull" for remote to local. Default is set to push.', required=False, type=str)
@click.option('-o', '--options', 'rsync_options', help='a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr', required=False, type=str)
def parallel_rsync(nchannels, local_path, remote_path, password, rsync_options='-vcr', direction='push'):
    cluster = LocalCluster()
    client = Client(cluster)
    prsync(nchannels=nchannels, local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction,  client=client)
    return 0


@click.command()
@click.option('-d', '--data-path', 'data_path', help='The path to a directory containing multiple fastq files.', required=True, type=str)
@click.option('-r', '--reference', 'reference', help='The path to your reference file', required=True, type=str)
@click.option('-p', '--password', 'password', help='The basecaller you plan to use. ["albacore", "guppy-cpu", "guppy-gpu"]', required=True, type=str)
@click.option('-d', '--direction', 'direction', help='Default is set to push- pull not yet implemented', required=False, type=str)
@click.option('-c', '--client', 'client', help='By default the client is set to local cluster', required=False, type=str)
@click.option('-o', '--options', 'rsync_options', help='a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr', required=False, type=str)
@click.argument('scheduler_address', required=True, help="A scheduler address can be obtained with the build_cluster command.")
def parallel_minimap2(scheduler_address, input_path, reference, save_path, command):
    return 0

