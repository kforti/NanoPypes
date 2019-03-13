import logging
import time
from dask_jobqueue import LSFCluster
from distributed import progress, Client, LocalCluster

from nanopypes.config import ComputeConfig


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
        self.ncpus = self.config.ncpus(ncpus)
        self.cluster_type = self.config.cluster_type(cluster_type)
        self.workers = self.config.workers(workers)
        self.scale_value = self.config.scale_value(scale_value)
        self.time_out = time_out

        if debug:
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    @property
    def settings(self):
        return self.__dict__

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
    def pending_jobs(self):
        return self.cluster.pending_jobs

    @property
    def running_jobs(self):
        return self.cluster.running_jobs

    @property
    def finished_jobs(self):
        return self.cluster.finished_jobs

    def scale(self, value):
        """Add workers to cluster connection"""
        self.cluster.scale(value)
        timer = 0
        pending_jobs = self.cluster.pending_jobs
        running_jobs = len(self.cluster.scheduler.workers)
        running_workers = len(self.cluster.running_jobs)

        while len(self.cluster.scheduler.workers) < int(value * 0.80):
            if timer == 0 or len(self.cluster.scheduler.workers) != running_jobs or len(self.cluster.running_jobs) != running_workers or pending_jobs != self.cluster.pending_jobs:
                running_jobs = len(self.cluster.scheduler.workers)
                running_workers = len(self.cluster.running_jobs)
                print("Client: ", self.client)
                print("workers: ", len(self.cluster.scheduler.workers))
                print("expected workers: ", value)
                print("pending jobs: ", self.cluster.pending_jobs)
                print("jobs: ", len(self.cluster.running_jobs))
            if timer > self.time_out:
                raise ConnectionError("Could not start all workers before time_out")
            time.sleep(1)
            timer += 1

        self.workers = value

    def map(self, func, iterable, show_progress=True):
        self.futures = self.client.map(func, iterable)
        if show_progress == True:
            progress(self.futures)
        futures = [self.client.gather(future) for future in self.futures]
        return futures

    def show_progress(self):
        progress(self.futures)

    def connect(self):
        """ Establish connection to cluster"""
        # assert self.workers != None, "You must assign number of workers"
        # assert self.queue != None, "You must assign a queue to run your workers on"

        if self.cluster_type == "LSF":
            logging.info("connecting to cluster")
            self.cluster = LSFCluster(queue=self.queue, #Passed to #BSUB -q option.
                                      project=self.project, #Passed to #BSUB -P option.
                                      processes=self.workers,
                                      walltime=self.walltime, #Passed to #BSUB -W option.
                                      ncpus=self.ncpus, #Passed to #BSUB -n option.
                                      mem=self.mem, #Passed to #BSUB -M option.
                                      cores=self.cores,
                                      memory=self.memory,
                                      death_timeout=self.time_out)
        elif self.cluster_type == "local":
            self.cluster = LocalCluster()
            self.workers = self.cluster.workers
        # print("job script: ", self.cluster.job_script())
        self.client = Client(self.cluster)
        # print("scale_value: ", self.scale_value)
        if self.scale_value:
            self.scale(self.scale_value)

    def stop_jobs(self, jobs="all"):
        if jobs == "all":
            self.cluster.stop_all_jobs()
        else:
            self.cluster.stop_jobs(jobs)

    def close(self):
        self.client.close()
        self.cluster.close()
