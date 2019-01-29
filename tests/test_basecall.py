import unittest
import time
from nanopypes.albacore import Cluster, Albacore
from nanopypes.nanopypes import *


class TestBasecall(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass


    def test_000_basecall(self):
        """Build a cluster object with yaml"""
        yaml = "basecall_test_config.yml"
        cluster = Cluster(config=yaml)
        albacore = Albacore(input=yaml)

        basecall(albacore, cluster)
