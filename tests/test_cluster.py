import unittest
import yaml

from nanopypes.compute import ClusterManager

from distributed import Client
import time



def test_cluster_from_dict():
    expected_cluster = {'cluster_type': 'lsf', 'job_time': '01:00', 'project': '/project/umw_athma_pai', 'queue': 'short', 'workers_per_job': 10, 'min_num_workers': None, 'num_workers': 10, 'worker_cores': 10, 'worker_memory': 2048, 'time_out': None, 'job_extra': None, 'env_extra': None}

    cluster_config_path = 'test_configs/lsf.yml'
    with open(cluster_config_path, 'r') as file:
        config = yaml.safe_load(file)["compute"]["cluster1"]
        #print(config)
    cluster = ClusterManager.from_dict(config)
    assert cluster == expected_cluster


def test_lsf_cluster_build():
    from distributed import LocalCluster
    expected_job_script = '#!/bin/bash\n\n#BSUB -J dask-worker\n#BSUB -q short\n#BSUB -n 12\n#BSUB -R "span[hosts=1]"\n#BSUB -M 8000\n#BSUB -W 4:00\nJOB_ID=${LSB_JOBID%.*}\n\n\n\n/share/pkg/python3/3.5.0/bin/python3 -m distributed.cli.dask_worker tcp://10.192.23.85:41273 --nthreads 3 --nprocs 4 --memory-limit 2.00GB --name dask-worker--${JOB_ID}-- --death-timeout 60\n'
    cm = ClusterManager(num_workers=8, worker_memory=2048, worker_cores=3, cluster_type='lsf', queue='short',
                        workers_per_job=4, job_time='4:00')
    client = cm.start_cluster()
    assert cm.cluster.job_script() == expected_job_script
    start = time.perf_counter()
    cluster = LocalCluster()
    cluster.

    while True:
        try:
            assert cm.cluster.worker_cores == 12
            break
        except AssertionError:
            pass
        if (time.perf_counter() - start) > 150.0:
            raise TimeoutError
        time.sleep(10)


##########################################################################
### Helper Functions
##########################################################################
if __name__ == '__main__':
    test_cluster_from_dict()
    test_lsf_cluster_build()
