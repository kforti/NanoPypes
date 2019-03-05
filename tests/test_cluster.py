import unittest
import time
from nanopypes.albacore import Cluster


class TestCluster(unittest.TestCase):
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
        self.cluster = Cluster(config="build_command_test.yml")
        self.cluster.connect()

        expected_workers = self.cluster.expected_workers
        actual_workers = self.cluster.connected_workers
        print("expected workers: ", expected_workers)
        print("actual workers: ", actual_workers)
        self.assertTrue(expected_workers == actual_workers)

        self.cluster.stop_jobs()
        print("Stopping workers")
        timer = 0
        while len(self.cluster.running_jobs) > 1:
            print("Finished jobs", self.cluster.finished_jobs)
            print("jobs", self.cluster.running_jobs)
            print("time", timer)
            timer += 1
            time.sleep(1)
            if timer > 30:
                break

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
    #     self.cluster = Cluster(config="build_command_test.yml",
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
        self.cluster = Cluster(config="build_command_test.yml")
        self.cluster.connect()
        self.cluster.map(increment, range(500))
        self.cluster.show_progress()


##########################################################################
### Helper Functions
##########################################################################

def increment(i):
    time.sleep(1)
    return i + 1
