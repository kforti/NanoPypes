from dask_jobqueue import LSFCluster
from distributed import Client, LocalCluster

import logging

def get_config_file(config_type):
    """config_types {'lsf': 'configs/lsf'}"""
    raise NotImplementedError


class ClusterManager:
    """ Cluster based task manager for running the basecaller in parallel"""
    def __init__(self, num_workers=None, worker_memory=None, worker_cores=None, cluster_type=None,
                 queue=None, workers_per_job=None, job_time=None, project=None, min_num_workers=None,
                 time_out=2000, job_extra=None, env_extra=None, cluster=None, debug=False, interaface=None):
        self.cluster_type = cluster_type
        self.queue = queue
        self.num_workers = num_workers or len(cluster.workers) or 0
        self.worker_memory = worker_memory
        self.worker_cores = worker_cores
        self.workers_per_job = workers_per_job
        self.job_time = job_time
        self.project = project
        self.min_num_workers = min_num_workers
        self.time_out = time_out
        self.env_extra = env_extra
        self.interface = None
        self.clients = []

        if debug:
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
            if self.cluster_type == 'lsf':
                if job_extra:
                    job_extra.append("-o dask_lsf_cluster.err")
                    job_extra.append("-o dask_lsf_cluster.out")
                else:
                    job_extra = ["-o dask_lsf_cluster.err", "-o dask_lsf_cluster.out"]
        self.job_extra = job_extra

        self._cluster = cluster or self.build_cluster() # Must be explicitly built first, or a cluster object can be passed

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        setattr(instance, 'clients', [])
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
            assert self.cluster is not None
        except:
            self.build_cluster()

        minimum_workers = self.min_num_workers or int(0.5 * self.num_workers)
        self.cluster.scale(self.num_workers)
        return self.client

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
                             job_extra=['-R "rusage[mem={}]"'.format(self.worker_memory), '-o dask_worker.out',
                                             '-e dask_worker.err'],
                             cores=ncpus,
                             memory=dask_memory)
        return cluster

    def _build_slurm(self):
        pass

    def close(self):
        for client in self.clients:
            client.close()
        self.cluster.close()
