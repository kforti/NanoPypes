import logging
import time
import math

from dask_jobqueue import LSFCluster
from distributed import Client, LocalCluster

from nanopypes.config import ComputeConfig

import logging


class Cluster:
    """ Cluster based task manager for running the basecaller in parallel"""
    def __init__(self, config=None, queue=None, project=None, job_time=None, cores=None, mem=None,
                 ncpus=None, memory=None, workers=None, scale_value=None, cluster_type=None,
                 time_out=2000, debug=False):
        if config:
            self.config = config
        else:
            self.config = ComputeConfig(settings=None)
        self.queue = self.config.queue(queue)
        self.project = self.config.project(project)
        self.walltime = self.config.job_time(job_time)
        self.cores = self.config.cores(cores)
        self.memory = self.config.memory(memory)
        self.mem = self.config.mem(mem)
        if self.mem:
            self.umass_mem = int(math.ceil(self.mem / 1048576))
        self.ncpus = self.config.ncpus(ncpus)
        self.cluster_type = self.config.cluster_type(cluster_type)
        self.workers = self.config.workers(workers)
        self.scale_value = self.config.scale_value(scale_value)
        self.time_out = time_out
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    @property
    def expected_workers(self):
        return self.workers

    @expected_workers.setter
    def expected_workers(self, value):
        self.workers = value

    @property
    def connected_workers(self):
        return len(self.cluster.scheduler.workers)

    @property
    def num_pending_jobs(self):
        return self.cluster.pending_jobs

    @property
    def num_running_jobs(self):
        return self.cluster.running_jobs

    @property
    def num_finished_jobs(self):
        return self.cluster.finished_jobs

    def scale(self, value):
        """Add workers to cluster connection"""
        print("scaling cluster....")
        self.cluster.scale(value)
        timer = 0
        pending_jobs = self.cluster.pending_jobs
        running_jobs = len(self.cluster.scheduler.workers)
        running_workers = len(self.cluster.running_jobs)

        while len(self.cluster.scheduler.workers) < int(value * 0.5):
            if timer == 0 or len(self.cluster.scheduler.workers) != running_jobs or len(self.cluster.running_jobs) != running_workers or pending_jobs != self.cluster.pending_jobs:
                running_jobs = len(self.cluster.scheduler.workers)
                running_workers = len(self.cluster.running_jobs)
                # print("Client: ", self.client)
                print("workers: ", len(self.cluster.scheduler.workers))
                print("expected workers: ", value)
                print("pending jobs: ", self.cluster.pending_jobs)
                print("jobs: ", len(self.cluster.running_jobs))
            if timer > self.time_out:
                raise ConnectionError("Could not start all workers before time_out")
            time.sleep(1)
            timer += 1

        self.workers = value

    def connect(self):
        """ Establish connection to cluster"""
        if self.cluster_type == "LSF":
            logging.info("connecting to LSF cluster")
            self.cluster = LSFCluster(queue=self.queue, #Passed to #BSUB -q option.
                                      project=self.project, #Passed to #BSUB -P option.
                                      processes=self.workers,
                                      walltime=self.walltime, #Passed to #BSUB -W option.
                                      ncpus=self.ncpus, #Passed to #BSUB -n option.
                                      mem=self.mem, #Passed to #BSUB -M option.
                                      job_extra=['-R "rusage[mem={}]"'.format(self.umass_mem)],
                                      cores=self.cores,
                                      memory=self.memory,
                                      #interface='ib0',
                                      death_timeout=self.time_out)
            # print("job script: ", self.cluster.job_script())
            print("\nYour Scheduler's address: ", self.cluster.scheduler_address)
        elif self.cluster_type == "local":
            self.cluster = LocalCluster()
            self.workers = self.cluster.workers

        # self.client = Client(self.cluster)

        # print("scale_value: ", self.scale_value)
        if self.scale_value:
            self.scale(self.scale_value)

        return self.cluster.scheduler_address

    def stop_jobs(self, jobs="all"):
        if jobs == "all":
            self.cluster.stop_all_jobs()
        else:
            self.cluster.stop_jobs(jobs)

    def close(self):
        self.client.close()
        self.cluster.close()

