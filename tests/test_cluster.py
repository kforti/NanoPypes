import unittest
import time

from nanopypes.compute import Cluster
from nanopypes.config import Configuration

from distributed import Client

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
        cluster = Cluster(compute_config)
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
