#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""

import os
import shutil
import unittest
from pathlib import Path

from nanopypes.config import Configuration
from nanopypes.compute import Cluster

from distributed import Client, LocalCluster



########################################################################
### Test Minimap2 Pipe                                               ###
########################################################################
class TestMinimap2Pipe(unittest.TestCase):
    """Tests for the Albacore class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_albacore_commands(self):
        """Test the albacore commands that are generated from passing custom inputs."""
        pass
