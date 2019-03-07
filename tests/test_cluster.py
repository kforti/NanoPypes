import unittest
import time
from nanopypes.compute import Cluster
from nanopypes.config import Configuration


class TestClusterLocal(unittest.TestCase):
    """Tests for the Albacore class."""


    def setUp(self):
        """Set up test fixtures, if any."""
        self.compute = Cluster(config=None)
        self.compute.connect()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.compute.close()

    def test_000_build_cluster(self):
        """Build a cluster object with yaml"""
        expected_workers = 4
        actual_workers = self.compute.connected_workers
        self.assertTrue(expected_workers == actual_workers)

    def test_004_map(self):
        """ Test the map function on a cluster instance"""
        results = self.compute.map(increment, range(150))
        self.compute.show_progress()
        print(results)

class TestClusterRemote(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        self.compute = Cluster(config=None)
        self.compute.connect()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass


    def test_000_build_cluster(self):
        """Build a cluster object with yaml"""
        config = Configuration(config="test_configs/remote_basecall.yml")
        self.compute = Cluster(config)
        self.compute.connect()

        expected_workers = self.compute.expected_workers
        actual_workers = self.compute.connected_workers
        self.assertTrue(expected_workers == actual_workers)

        self.compute.close()


    # def test_001_build_cluster(self):
    #     """Build a cluster object with yaml"""
    #     self.cluster = Cluster(job_time="06:00",
    #                            memory="2 GB",
    #                            project="/project/umw_athma_pai",
    #                            queue="long",
    #                            workers=20,
    #                            cores=20,
    #                            scale_value=1,
    #                            mem=40000,
    #                            ncpus=20,
    #                            cluster_type="LSF",)
    #     self.cluster.connect()
    #
    #     expected_workers = self.cluster.expected_workers
    #     actual_workers = self.cluster.connected_workers
    #     print("expected workers: ", expected_workers)
    #     print("actual workers: ", actual_workers)
    #     self.assertTrue(expected_workers == actual_workers)
    #
    # def test_002_build_cluster(self):
    #     """Build a cluster object with yaml"""
    #     self.cluster = Cluster(config="local_builds.yml",
    #                            job_time="06:00",
    #                            memory="2 GB",
    #                            mem=40000,
    #                            cores=10,
    #                            workers=10,
    #                            ncpus=10,
    #                            cluster_type="LSF",)
    #     self.cluster.connect()
    #
    #     expected_workers = self.cluster.expected_workers
    #     actual_workers = self.cluster.connected_workers
    #     print("expected workers: ", expected_workers)
    #     print("actual workers: ", actual_workers)
    #     self.assertTrue(expected_workers == actual_workers)
    #     self.assertTrue(actual_workers == 10)

    def test_004_map(self):
        """ Test the map function on a cluster instance"""
        results = self.compute.map(increment, range(150))
        self.compute.show_progress()
        print(results)


##########################################################################
### Helper Functions
##########################################################################

def increment(i):
    time.sleep(1)
    return i + 1
