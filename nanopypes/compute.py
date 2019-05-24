from dask_jobqueue import LSFCluster
from distributed import Client


def get_config_file(config_type):
    """config_types {'lsf': 'config_templates/lsf'}"""
    raise NotImplementedError

class NanopypesCluster:
    """ Cluster based task manager for running the basecaller in parallel"""
    def __init__(self, num_workers=None, worker_memory=None, worker_cores=None, cluster_type=None,
                 queue=None, workers_per_job=None, job_time=None, project=None, min_num_workers=None,
                 time_out=2000, job_extra=None, env_extra=None, cluster=None, logging=False):
        self.workers = num_workers
        self.cluster_type = cluster_type.lower()
        self.cluster = cluster or self.build_cluster() # Must be explicitly built first, or a cluster object can be passed
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
        self.clients = []

        if logging:
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
            if self.cluster_type == 'lsf':
                if job_extra:
                    job_extra.append("-o dask_lsf_cluster.err")
                    job_extra.append("-o dask_lsf_cluster.out")
                else:
                    job_extra = ["-o dask_lsf_cluster.err", "-o dask_lsf_cluster.out"]
        self.job_extra = job_extra

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        return instance

    @property
    def expected_workers(self):
        return self.workers

    @property
    def connected_workers(self):
        c_workers = len(self.cluster.scheduler.workers)
        return c_workers

    @property
    def cluster_clients(self):
        return self.clients

    @property
    def cluster(self):
        return self.cluster

    def build_cluster(self, cluster_type=None):
        if self.cluster_type == 'lsf':
            cluster = self._build_lsf()

        elif self.cluster_type == 'slurm':
            cluster = self._build_slurm()

    def start_cluster(self):
        minimum_workers = self.min_num_workers or int(0.5 * self.num_workers)
        self.cluster.adapt(minimum=minimum_workers, maximum=self.num_workers)
        client = Client(self.cluster)
        self.clients.append(client)

        return client

    def _build_lsf(self):
        ncpus = self.workers_per_job * self.worker_cores
        mem_bytes = self.worker_memory * self.workers_per_job * 1024**2
        dask_memory = str(self.worker_memory / 1024) + 'GB'
        cluster = LSFCluster(queue=self.queue,  # Passed to #BSUB -q option.
                                  project=self.project,  # Passed to #BSUB -P option.
                                  processes=self.workers_per_job,
                                  walltime=self.walltime,  # Passed to #BSUB -W option.
                                  ncpus=ncpus,  # Passed to #BSUB -n option.
                                  mem=mem_bytes,  # Passed to #BSUB -M option.
                                  job_extra=['-R "rusage[mem={}]"'.format(self.worker_memory), '-o dask_worker.out',
                                             '-e dask_worker.err'],
                                  cores=ncpus,
                                  memory=dask_memory,
                                  # interface='ib0',
                                  death_timeout=self.time_out,
                                  env_extra=self.env_extra)
        return cluster

    def _build_slurm(self):
        pass

    def close(self):
        for client in self.clients:
            client.close()
        self.cluster.close()





