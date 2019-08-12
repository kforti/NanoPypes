from dask_jobqueue import LSFCluster, SLURMCluster
from distributed import Client, LocalCluster
from dask_kubernetes import KubeCluster

from nanopypes.utilities import ComputeConfiguartion

import logging
import os



class ClusterManager:
    """ Cluster based task manager for running the basecaller in parallel"""
    def __init__(self, cluster_id=None, num_workers=0, worker_memory=None, worker_cores=None, cluster_type=None,
                 queue=None, workers_per_job=None, job_time=None, project=None, min_num_workers=None,
                 time_out=2000, job_extra=None, env_extra=None, cluster=None, debug=False, interaface=None):
        self.cluster_id = cluster_id or cluster_type
        self.cluster_type = cluster_type
        self.queue = queue
        self.num_workers = num_workers
        self.worker_memory = worker_memory
        self.worker_cores = worker_cores
        self.workers_per_job = workers_per_job
        self.job_time = job_time
        self.project = project
        self.min_num_workers = min_num_workers
        self.time_out = time_out
        self.env_extra = env_extra
        try:
            self.core_memory = str(int(self.worker_memory / self.worker_cores))
        except:
            "There was an error in assigning memory per core..."
            pass
        self.interface = None
        self.clients = []

        if debug:
            self.job_extra = self._set_debug(job_extra)
        else:
            self.job_extra = job_extra or ['-R rusage[mem={}]'.format(self.core_memory)]

        self._cluster = cluster #or self.build_cluster() # Must be explicitly built first, or a cluster object can be passed

    def _set_debug(self, job_extra):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        if self.cluster_type == 'lsf':
            if job_extra:
                job_extra.append("-o nanopypes_dask_{}.err".format(self.cluster_id))
                job_extra.append("-o nanopypes_dask_{}.out".format(self.cluster_id))
                job_extra.append('-R rusage[mem={}]'.format(self.core_memory))
            else:
                job_extra = ['-R rusage[mem={}]'.format(self.core_memory), "-o dask_lsf_cluster.err", "-o dask_lsf_cluster.out"]
        return job_extra

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls(**config_dict)
        return instance

    @classmethod
    def from_config_file(cls, id, path="configs/compute.yml", **kwargs):
        if path == "configs/compute.yml":
            path = os.path.join(os.path.dirname(__file__), path)

        cc = ComputeConfiguartion(id, path, **kwargs)
        config = cc.config
        instance = cls(**config)
        return instance

    @property
    def expected_workers(self):
        try:
            num = max(self.num_workers, len(self.cluster.workers))
        except AttributeError:
            num = max(self.num_workers, self.cluster.worker_processes)
        return num

    @property
    def connected_workers(self):
        workers = len(self.cluster.scheduler.workers)
        return workers

    @property
    def cluster_clients(self):
        return self.clients

    @property
    def cluster(self):
        return self._cluster

    def build_cluster(self, cluster_type=None):
        if self.cluster_type.lower() == 'lsf':
            cluster = self._build_lsf()

        elif self.cluster_type.lower() == 'slurm':
            cluster = self._build_slurm()

        elif self.cluster_type.lower() == 'local':
            cluster = LocalCluster()
            self.num_workers = len(cluster.scheduler.workers)
        self._cluster = cluster

        return

    def start_cluster(self):
        try:
            assert self.cluster
        except:
            self.build_cluster()
        #
        minimum_workers = self.min_num_workers or int(0.5 * self.num_workers)
        self._cluster.scale(self.num_workers)
        self._cluster.adapt(minimum=self.num_workers, maximum=self.num_workers)

        self.cluster.scheduler
        return self.client

    def scale(self, workers=None):
        workers = workers or self.num_workers
        self.cluster.scale()
        while self.cluster.scheduler.workers < workers:
            pass



    @property
    def client(self):
        client = Client(self.cluster)
        self.clients.append(client)

        return client

    def _build_lsf(self):
        ncpus = self.workers_per_job * self.worker_cores
        mem_bytes = self.worker_memory * self.workers_per_job * 1024**2
        dask_memory = str(int((self.worker_memory * self.workers_per_job)/ 1024)) + 'GB'
        cluster = LSFCluster(queue=self.queue, # Passed to #BSUB -q option.
                             project=self.project, # Passed to #BSUB -P option.
                             processes=self.workers_per_job,
                             walltime=self.job_time,# Passed to #BSUB -W option.
                             job_extra=self.job_extra,
                             cores=ncpus,
                             memory=dask_memory)
        return cluster

    def _build_slurm(self):
        ncpus = self.workers_per_job * self.worker_cores
        mem_bytes = self.worker_memory * self.workers_per_job * 1024 ** 2
        dask_memory = str(int((self.worker_memory * self.workers_per_job)/ 1024)) + 'GB'
        cluster = SLURMCluster(queue=self.queue,
                               project=self.project,
                               walltime=self.job_time,
                               job_cpu=ncpus,
                               job_mem=mem_bytes,
                               job_extra=self.job_extra,
                               processes=self.workers_per_job,
                               memory=dask_memory)
        return cluster

    def _build_kubernetes(self):
        ncpus = self.workers_per_job * self.worker_cores
        mem_bytes = self.worker_memory * self.workers_per_job * 1024 ** 2
        dask_memory = str(int((self.worker_memory * self.workers_per_job) / 1024)) + 'GB'
        cluster = KubeCluster(n_workers=self.num_workers,
                              )

    def close(self):
        for client in self.clients:
            client.close()
        self.cluster.close()

if __name__ == '__main__':
    # cluster = LocalCluster()
    # print(cluster.scheduler.workers)
    import os

    path = "configs/compute.yml"
    dir_name = os.path.dirname(__file__)
    print(dir_name)
    path = os.path.join(dir_name, path)
    print(path)

