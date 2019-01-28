import unittest
import time
from nanopypes.albacore import Cluster


class TestCluster(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.cluster.stop_jobs()
        time.sleep(30)

    def test_000_build_cluster(self):
        """Build a cluster object with yaml"""
        self.cluster = Cluster(config="build_command_test.yml")
        self.cluster.connect_workers()
        time.sleep(30)
        expected_workers = self.cluster.num_workers
        actual_Workers = self.cluster.connected_workers
        self.assertTrue(expected_workers == actual_Workers)

    def test_001_build_cluster(self):
        """Build a cluster object and add workers"""
        self.cluster = Cluster(job_time="06:00", memory="2 GB", project="/project/umw_athma_pai",
                          queue="long", workers=10, cores=1)
        self.cluster.connect_workers()
        time.sleep(30)
        expected_workers = self.cluster.num_workers
        actual_Workers = self.cluster.connected_workers
        self.assertTrue(expected_workers == actual_Workers)

    def test_002_build_cluster(self):
        """Build a cluster object and add workers"""
        self.cluster = Cluster(config="build_command_test.yml",
                          queue="long", workers=10, cores=1)
        self.cluster.connect_workers()
        time.sleep(30)
        expected_workers = self.cluster.num_workers
        actual_Workers = self.cluster.connected_workers
        self.assertTrue(expected_workers == actual_Workers)

    def test_003_connect_workers(self):
        """Build a cluster object and add workers"""
        add_workers = 10
        self.cluster = Cluster(config="build_command_test.yml")
        num_workers = self.cluster.num_workers
        expected_workers = add_workers + num_workers
        self.cluster.add_workers(num=add_workers)
        self.cluster.connect_workers()
        time.sleep(30)
        actual_workers = self.cluster.connected_workers
        self.assertTrue(expected_workers == actual_workers)