# -*- coding: utf-8 -*-
"""Console script for pai-nanopypes."""
import click

from nanopypes.run_pipes import albacore_basecaller


@click.command()
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
@click.option('-s', '--data_splits', multiple=True, help='the number of splits to divide raw minion sequence batches into. Start with the number of workers you intend to use and optimize from there', required=True, type=int)
@click.option('-b', '--batch_bunches', multiple=True, help="The number of batches to process at one time.", type=int)
@click.option('-c', '--continue_on', multiple=True, help="if True then the basecaller will continue from it's previous start location.", type=bool)
@click.argument('config', required=False)
def albacore_basecaller(config, data_splits, batch_bunches, continue_on=False, pypes_log=None):
    """Console script for running the albacore parallel basecaller."""
    bc_data = albacore_basecaller(config=config,
                                  data_splits=data_splits,
                                  batch_bunch=batch_bunches)
    return 0













    ##########################################################################################################
    #Raw Fast5 Data
    ##########################################################################################################
    # input_path = basecall_config.input_path
    # sample_data = Sample(input_path)
    #
    # ###########################################################################################################
    # # Albacore
    # ###########################################################################################################
    # kit = basecall_config.kit
    # save_path = basecall_config.save_path
    # flowcell = basecall_config.flowcell
    # barcoding = basecall_config.barcoding
    # worker_threads = basecall_config.worker_threads
    # output_format = basecall_config.output_format
    # recursive = basecall_config.recursive
    #
    # ###########################################################################################################
    # # ClusterBasecaller
    # ###########################################################################################################
    # queue = basecall_config.queue
    # project = basecall_config.project
    # job_time = basecall_config.job_time
    # workers = basecall_config.workers
    # ncpus = basecall_config.ncpus
    # mem = basecall_config.mem
    # cores = basecall_config.cores
    # memory = basecall_config.memory
    #
    # ###########################################################################################################
    # # Build Objects
    # ###########################################################################################################
    # click.echo("Building Albacore")
    # albacore = Albacore(sample_data, flowcell, kit, save_path, output_format, barcoding)
    # click.echo("Connecting to cluster")
    # cluster = Cluster(queue, project, job_time, workers, cores, memory)
    # click.echo("Running basecaller")
    # basecall(albacore, cluster)






# if __name__ == '__main__':
#     albacore_basecaller()
