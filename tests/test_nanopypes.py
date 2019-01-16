#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""


import unittest
from click.testing import CliRunner
from nanopypes.albacore import Albacore
from nanopypes.cli import main

class TestDataHandling(unittest.TestCase):
    """Tests for the data handling within the `pai-nanopypes` package."""

    @classmethod
    def setUp(self):
        """Set up the test data, if not there."""
        import os
        from pathlib import Path

        results_path = Path("test_data/results")
        if not results_path.exists():
            results_path.mkdir()
            build_test_data(results_path)





    @classmethod
    def tearDown(self):
        """Tear down test fixtures, if any."""


    def test_000_collapse_save(self):
        """Test for collapsing the saved data directories after the parallel basecalling."""


class TestAlbacore(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        from nanopypes.albacore import Albacore

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_albacore_commands(self):
        """Test the albacore commands that are generated."""
        albacore = Albacore(input='./test_data/',
                            flowcell='FLO-MIN106',
                            kit='SQK-LSK109',
                            save_path='./test_data/basecalled_data/',
                            output_format='fast5',
                            barcoding=True,
                            )

        command = albacore.build_command('./test_data/', './test_data/basecalled_data/')
        self.assertTrue("read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fast5"
                        " --save_path ./test_data/basecalled_data/ --worker_threads 1 --input ./test_data/ --barcoding " == command)

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(main)
        assert result.exit_code == 0
        assert 'pai-nanopypes.cli.main' in result.output
        help_result = runner.invoke(main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


########################################################################
### Helper Functions                                                 ###
########################################################################

def build_test_data(path):
    """Function to build test data."""
    dir_children = ["configuration.cfg",
                    "pipeline.log",
                    "sequencing_summary.txt",
                    "sequencing_telemetry.js",
                    "workspace",]

    for i in range(10):
        dir_name = str(i)
        dir_path = path.joinpath(dir_name)
        dir_path.mkdir()

        for name in dir_children:
            name_path = dir_path.joinpath(name)
            if "." in name:
                name_path.t







unittest.main()
