# -*- coding: utf-8 -*-
"""Console script for pai-nanopypes."""
import shutil
import os

import click

from nanopypes.run_pipes import albacore_basecaller as albacore
from nanopypes.run_pipes import ParallelRsync as prsync



# @click.option('--basecaller', help='Select the basecaller you would like to use')
# @click.option('--location', help='run the basecaller from local or cluster environment')
# @click.option('--kit', help='the kit used in the MinION sequencing run')
# @click.option('--flowcell', help='the flowcell used in the MinION sequencing run')
# @click.option('--input_path', help='the input path for the Sample/Run containing the Raw MinION sequencing data')
# @click.option('--save_path', help='the path for results of the basecalling to be saved to')
# @click.option('--barcoding', help='select whether or not your samples are barcoded')
# @click.option('--output_format', help='select fast5 or fastq output format')
# @click.option('--worker_threads', help='number of worker threads selected for the albacore software; different from dask workers')
# @click.option('--recursive', help='is your data a directory of directories? If yes, select True')
# @click.option('--job_time', help='the amount of time you expect the overall basecalling to take')
# @click.option('--mem', help='memory per node')
# @click.option('--ncpus', help='the number of cpus on the cluster')
# @click.option('--project', help='the project on the cluster where your input data and/or save data are located')
# @click.option('--queue', help='the queue to run each job on the cluster')
# @click.option('--workers', help='the amount of dask workers')
# @click.option('--cores', help='the number of cores per dask worker')
# @click.option('--memory', help='the amount of memory per dask worker')
@click.command()
@click.option('-s', '--data-splits', 'data_splits', help='the number of splits to divide raw minion sequence batches into. Start with the number of workers you intend to use and optimize from there', required=True, type=int)
@click.option('-b', '--batch-bunches', 'batch_bunches', help="The number of batches to process at one time.", type=int)
@click.option('-c', '--continue-on', 'continue_on', help="if True then the basecaller will continue from it's previous start location.", type=bool)
@click.argument('config', required=True)
def albacore_basecaller(config, data_splits, batch_bunches, continue_on=False):
    """Console script for running the albacore parallel basecaller."""
    bc_data = albacore(config=config,
                       data_splits=data_splits,
                       batch_bunch=batch_bunches,
                       continue_on=continue_on)
    return 0


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
@click.option('-l', '--local-path', 'local_path', help='The path to the data on your local machine.', required=True, type=str)
@click.option('-r', '--remote-path', 'remote_path', help='The path to where your data should be saved remotely, must include username', required=True, type=str)
@click.option('-p', '--password', 'password', help='The basecaller you plan to use. ["albacore", "guppy-cpu", "guppy-gpu"]', required=True, type=str)
@click.option('-d', '--direction', 'direction', help='Default is set to push- pull not yet implemented', required=False, type=str)
@click.option('-c', '--client', 'client', help='By default the client is set to local cluster', required=False, type=str)
@click.option('-o', '--options', 'rsync_options', help='a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr', required=False, type=str)
def parallel_rsync(local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):
    prsync(local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction,  client=client)
    return 0


@click.command()
@click.option('-d', '--data-path', 'data_path', help='The path to a directory containing multiple fastq files.', required=True, type=str)
@click.option('-r', '--reference', 'reference', help='The path to your reference file', required=True, type=str)
@click.option('-p', '--password', 'password', help='The basecaller you plan to use. ["albacore", "guppy-cpu", "guppy-gpu"]', required=True, type=str)
@click.option('-d', '--direction', 'direction', help='Default is set to push- pull not yet implemented', required=False, type=str)
@click.option('-c', '--client', 'client', help='By default the client is set to local cluster', required=False, type=str)
@click.option('-o', '--options', 'rsync_options', help='a string containing the rsync options you would like to use, must include the appropriate flag(s). Default options are -vcr', required=False, type=str)
def parallel_minimap2(local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):
    prsync(local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction,  client=client)
    return 0
