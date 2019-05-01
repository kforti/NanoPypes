#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""

import os
import shutil
import unittest
from pathlib import Path

from nanopypes.config import Configuration
from nanopypes.compute import Cluster
from nanopypes.pipes.variant_calling import VariantCalling

from distributed import Client, LocalCluster



########################################################################
### Test Minimap2 Pipe                                               ###
########################################################################
class TestVariantCallingPipeRemote(unittest.TestCase):
    """Tests for the Albacore class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_variant_calling(self):
        """Test the albacore commands that are generated from passing custom inputs."""
        config = Configuration(config="test_configs/remote_builds.yml")
        compute_config = config.get_compute("cluster1")
        cluster = Cluster(compute_config, umass_mem=2480, logs=True)
        scheduler_address = cluster.connect()
        client = Client(scheduler_address)

        v = VariantCalling(input_path='test_data/minimap/sam_files',
                           reference='test_data/minimap/references/Plasmodium_falciparum_3D7.fasta',
                           client=client, save_path='test_data/minimap/variant_calling_output',
                           input_type='sam')
        v()
        return
