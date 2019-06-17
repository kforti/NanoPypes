import unittest
import time
import yaml

from nanopypes.compute import ClusterManager
from config import Configuration

from distributed import Client




def test_cluster_from_dict():
    expected_cluster = {'cluster_type': 'lsf', 'job_time': '01:00', 'project': '/project/umw_athma_pai', 'queue': 'short', 'workers_per_job': 10, 'min_num_workers': None, 'num_workers': 10, 'worker_cores': 10, 'worker_memory': 2048, 'time_out': None, 'job_extra': None, 'env_extra': None}

    cluster_config_path = 'test_configs/lsf.yml'
    with open(cluster_config_path, 'r') as file:
        config = yaml.safe_load(file)["compute"]["cluster1"]
        #print(config)
    cluster = ClusterManager.from_dict(config)
    assert cluster == expected_cluster






class TestClusterLocal(unittest.TestCase):
    """Tests for the Albacore class."""


    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_000_build_cluster(self):
        """Build a cluster object with yaml"""
        compute = Cluster(config=None)
        scheduler_address = self.compute.connect()
        client = Client(scheduler_address)
        expected_workers = 4
        actual_workers = compute.connected_workers
        self.assertTrue(expected_workers == actual_workers)
        client.close()
        return

class TestClusterRemote(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass


    def test_000_build_cluster(self):
        """Build a cluster object with yaml"""
        time_out = 100

        config = Configuration(config="test_configs/remote_builds.yml")
        compute_config = config.get_compute("cluster1")
        cluster = Cluster(compute_config, umass_mem=2480, logs=True)
        scheduler_address = cluster.connect()
        client = Client(scheduler_address)
        expected_workers = cluster.expected_workers
        timer = 0
        while expected_workers > cluster.connected_workers:
            if timer == 100:
                raise TimeoutError("All workers did not connect within {}s".format(time_out))
            time.sleep(1)
            timer += 1

        self.assertTrue(expected_workers == cluster.connected_workers)
        client.close()
        return


    def test_001_build_cluster(self):
        """Build a cluster object with pure python"""
        pass


##########################################################################
### Helper Functions
##########################################################################
if __name__ == '__main__':
    test_cluster_from_dict()
