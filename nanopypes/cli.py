# -*- coding: utf-8 -*-

"""Console script for pai-nanopypes."""
import sys
import logging
from datetime import datetime
from nanopypes.objects import Sample
from nanopypes.albacore import Albacore, Cluster
import click
from yaml import load
from nanopypes.nanopypes import basecall

# logging.basicConfig(filename='tests/logging/commandline.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Config:
    def __init__(self, config):
        self._config = self.parse_config(config)

    @property
    def config(self):
        return self._config

    @property
    def basecall_config(self):
        return self._config["basecall_config"]

    def parse_config(self, config):
        extension = config.split('.')[1]
        if extension == "yml":
            file = open(config, "r")
            return load(file)

class BasecallConfig(Config):

    def __init__(self, config, **kwargs):
        print("setting configuration...")
        super().__init__(config)
        self.bc_config = super().basecall_config
        self._parse_kwargs(**kwargs)

        logger.info("Basecall command initiated at %s with settings: %s" % (datetime.now(), self.bc_config))

    def _parse_kwargs(self, **kwargs):
        """parse the kwargs passed into the config and update
        the config settings based on the arguments passed"""
        for key, value in kwargs.items():
            if value != None and key != "config":
                self.bc_config[key] = value
            else:
                continue

    @property
    def kit(self):
        return self.bc_config["kit"]

    @property
    def flowcell(self):
        return self.bc_config["flowcell"]

    @property
    def save_path(self):
        return self.bc_config["save_path"]

    @property
    def input_path(self):
        return self.bc_config["input_path"]

    @property
    def barcoding(self):
        return self.bc_config["barcoding"]

    @property
    def output_format(self):
        return self.bc_config["output_format"]

    @property
    def worker_threads(self):
        return self.bc_config["worker_threads"]

    @property
    def recursive(self):
        return self.bc_config["recursive"]

    #######################################################################
    ## Cluster properties
    #######################################################################

    @property
    def ncpus(self):
        return self.bc_config["cluster"]["ncpus"]

    @property
    def job_time(self):
        return self.bc_config["cluster"]["job_time"]

    @property
    def mem(self):
        return self.bc_config["cluster"]["mem"]

    @property
    def project(self):
        return self.bc_config["cluster"]["project"]

    @property
    def queue(self):
        return self.bc_config["cluster"]["queue"]

    @property
    def workers(self):
        return self.bc_config["cluster"]["workers"]

    @property
    def cores(self):
        return self.bc_config["cluster"]["cores"]

    @property
    def memory(self):
        return self.bc_config["cluster"]["memory"]

@click.command()
@click.option('--location', help='run the basecaller from local or cluster environment')
@click.option('--kit', help='the kit used in the MinION sequencing run')
@click.option('--flowcell', help='the flowcell used in the MinION sequencing run')
@click.option('--input_path', help='the input path for the Sample/Run containing the Raw MinION sequencing data')
@click.option('--save_path', help='the path for results of the basecalling to be saved to')
@click.option('--barcoding', help='select whether or not your samples are barcoded')
@click.option('--output_format', help='select fast5 or fastq output format')
@click.option('--worker_threads', help='number of worker threads selected for the albacore software; different from dask workers')
@click.option('--recursive', help='is your data a directory of directories? If yes, select True')
@click.option('--job_time', help='the amount of time you expect the overall basecalling to take')
@click.option('--mem', help='memory per node')
@click.option('--ncpus', help='the number of cpus on the cluster')
@click.option('--project', help='the project on the cluster where your input data and/or save data are located')
@click.option('--queue', help='the queue to run each job on the cluster')
@click.option('--workers', help='the amount of dask workers')
@click.option('--cores', help='the number of cores per dask worker')
@click.option('--memory', help='the amount of memory per dask worker')
@click.argument('config', required=False)
def parallel_basecaller(config, **kwargs):
    """Console script for pai-nanopypes."""
    print("Configuring Basecaller...")
    basecall_config = BasecallConfig(config, **kwargs)

    ##########################################################################################################
    #Raw Fast5 Data
    ##########################################################################################################
    input_path = basecall_config.input_path
    sample_data = Sample(input_path)

    ###########################################################################################################
    # Albacore
    ###########################################################################################################
    kit = basecall_config.kit
    save_path = basecall_config.save_path
    flowcell = basecall_config.flowcell
    barcoding = basecall_config.barcoding
    worker_threads = basecall_config.worker_threads
    output_format = basecall_config.output_format
    recursive = basecall_config.recursive

    ###########################################################################################################
    # ClusterBasecaller
    ###########################################################################################################
    queue = basecall_config.queue
    project = basecall_config.project
    job_time = basecall_config.job_time
    workers = basecall_config.workers
    ncpus = basecall_config.ncpus
    mem = basecall_config.mem
    cores = basecall_config.cores
    memory = basecall_config.memory

    ###########################################################################################################
    # Build Objects
    ###########################################################################################################
    click.echo("Building Albacore")
    albacore = Albacore(sample_data, flowcell, kit, save_path, output_format, barcoding)
    click.echo("Connecting to cluster")
    cluster = Cluster(queue, project, job_time, workers, cores, memory)
    click.echo("Running basecaller")
    basecall(albacore, cluster)



    return 0


