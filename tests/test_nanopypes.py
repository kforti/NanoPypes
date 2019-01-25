#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""

import os
import shutil
import unittest
from pathlib import Path
from click.testing import CliRunner
from nanopypes.albacore import Albacore
from nanopypes.cli import parallel_basecaller
from nanopypes.utils import temp_dirs, remove_temps, collapse_save
from nanopypes.objects import Sample
from nanopypes.nanopypes import basecall

# class TestDataHandling(unittest.TestCase):
#     """Tests for the data handling within the `pai-nanopypes` package."""
#
#     @classmethod
#     def setUp(self):
#         """Set up the test data, if not there."""
#         import os
#         from pathlib import Path
#
#         results_path = Path("test_data/results")
#         if not results_path.exists():
#             results_path.mkdir()
#             build_test_data(results_path)
#
#
#
#
#
#     @classmethod
#     def tearDown(self):
#         """Tear down test fixtures, if any."""
#
#
#     def test_000_collapse_save(self):
#         """Test for collapsing the saved data directories after the parallel basecalling."""


class TestUtilityFunctions(unittest.TestCase):
    """Tests for the utility functions found in utils.py."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        # build_basecalled_test_data()
        # dirs = temp_dirs(data_dir="test_data/minion_sample_raw_data/fast5/pass/0",
        #                  temp_location="test_data/minion_sample_raw_data/")
        # assert dirs == ['test_data/basecalled_data/temp/0', 'test_data/basecalled_data/temp/1', 'test_data/basecalled_data/temp/2', 'test_data/basecalled_data/temp/3', 'test_data/basecalled_data/temp/4', 'test_data/basecalled_data/temp/5', 'test_data/basecalled_data/temp/6', 'test_data/basecalled_data/temp/7', 'test_data/basecalled_data/temp/8', 'test_data/basecalled_data/temp/9', 'test_data/basecalled_data/temp/10', 'test_data/basecalled_data/temp/11', 'test_data/basecalled_data/temp/12', 'test_data/basecalled_data/temp/13', 'test_data/basecalled_data/temp/14', 'test_data/basecalled_data/temp/15', 'test_data/basecalled_data/temp/16', 'test_data/basecalled_data/temp/17', 'test_data/basecalled_data/temp/18', 'test_data/basecalled_data/temp/19', 'test_data/basecalled_data/temp/20', 'test_data/basecalled_data/temp/21', 'test_data/basecalled_data/temp/22', 'test_data/basecalled_data/temp/23', 'test_data/basecalled_data/temp/24']


    def tearDown(self):
        """Tear down test fixtures, if any."""
        # shutil.rmtree("test_data/basecalled_data/temp")

    def test_000_temp_dirs(self):
        """Test the creation of temp dirs and distribution of the data into those dirs."""
        pass

    # def test_000_collapse_save(self):
    #     """Test the creation of t"""
    #     save_path = Path("test_data/basecalled_data/results")
    #     collapse_save(save_path)


class TestAlbacore(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        from nanopypes.albacore import Albacore

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_albacore_commands(self):
        """Test the albacore commands that are generated from passing custom inputs."""
        sample = Sample('test_data/minion_sample_raw_data/fast5/pass')
        save_path = './test_data/basecalled_data/results'
        albacore = Albacore(input=sample,
                            flowcell='FLO-MIN106',
                            kit='SQK-LSK109',
                            save_path=save_path,
                            output_format='fast5',
                            barcoding=True,
                            )

        command = albacore.build_command('./test_data/', '0')
        self.assertTrue("read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fast5"
                        " --save_path ./test_data/basecalled_data/results/0 --worker_threads 1 --input ./test_data/ --barcoding " == command)

        # func = albacore.build_func()
        # input_path = Path(albacore.input_path)
        # temp_path = input_path.joinpath("temp")
        #
        # for bin in albacore.bins:
        #     dirs = temp_dirs(bin, albacore.input_path)
        #     for dir in dirs:
        #         command = albacore.build_command(dir, bin.name)
        #         parallel_basecall_data(bin.name, dir, save_path)
        #     remove_temps(temp_path)

    def test_001_albacore_commands(self):
        """Test the albacore commands that are generated from passing yaml input."""
        yaml = "build_command_test.yml"
        albacore = Albacore(input=yaml)

        command = albacore.build_command('./test_data/', '0')
        self.assertTrue("read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fast5"
                        " --save_path ./test_data/basecalled_data/results/0 --worker_threads 1 --input ./test_data/ --barcoding " == command)

    # def test_003_basecall(self):
    #     """Test the albacore commands that are generated."""
    #     sample = Sample('test_data/minion_sample_raw_data/fast5/pass')
    #     save_path = './test_data/basecalled_data/results'
    #     albacore = Albacore(input=sample,
    #                         flowcell='FLO-MIN106',
    #                         kit='SQK-LSK109',
    #                         save_path=save_path,
    #                         output_format='fast5',
    #                         barcoding=True,
    #                         )
    #
    #     command = albacore.build_command('./test_data/', '0')
    #     self.assertTrue("read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fast5"
    #                     " --save_path ./test_data/basecalled_data/results/0 --worker_threads 1 --input ./test_data/ --barcoding " == command)
    #
    #     basecall(albacore, None)
    #
    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(parallel_basecaller)
    #     # assert result.exit_code == 0
    #     # assert 'pai-nanopypes.cli.parallel_basecaller' in result.output
    #     help_result = runner.invoke(parallel_basecaller, ['tests/test_data/umms_cluster_basecall.yml'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output


########################################################################
### Helper Functions                                                 ###
########################################################################

def build_basecalled_test_data(num_bins=10, reads_per_bin=100):
    """Function to build basecalle data"""
    dir_children = ["configuration.cfg",
                    "pipeline.log",
                    "sequencing_summary.txt",
                    "sequencing_telemetry.js",
                    "workspace",]
    names = ["pass", "fail", "calibration_strand"]

    for file in os.listdir("test_data/basecall_files"):
        shutil.move(("/".join(["test_data/basecall_files", file])), ("/".join(["test_data/basecalled_data", file])))

    workspace = Path("test_data/basecalled_data/workspace")

    if not workspace.exists():
        workspace.mkdir()

    for name in names:
        path = workspace.joinpath(name)
        if not path.exists():
            path.mkdir()

        for i in range(num_bins):
            dir_name = str(i)
            dir_path = path.joinpath(dir_name)
            if not dir_path.exists():
                dir_path.mkdir()

            for i in range(reads_per_bin):
                file_name = str(i)
                file_path = dir_path.joinpath(file_name)
                if not file_path.exists():
                    with open(file_path, "w") as f:
                        f.write("Some data......")

def parallel_basecall_data(bin, directory, save_path):

    basecall_files = {"config": "test_data/basecall_files/configuration.cfg",
                    "pipe": "test_data/basecall_files/pipeline.log",
                    "sum": "test_data/basecall_files/sequencing_summary.txt",
                    "tel": "test_data/basecall_files/sequencing_telemetry.js",
                      }

    workspace_dirs = ["pass", "fail", "calibration_strands"]
    directory = Path(directory)
    if not Path(save_path).exists():
        Path(save_path).mkdir()
    path = Path(save_path).joinpath(bin)
    if not path.exists():
        path.mkdir()
    save_path_contents = [i for i in os.listdir(path)]
    if save_path_contents == []:
        for file in basecall_files.keys():
            shutil.copy(basecall_files[file], path)
    workspace = path.joinpath("workspace")
    if not workspace.exists():
        workspace.mkdir()
    for name in workspace_dirs:
        read_type = workspace.joinpath(name)
        if not read_type.exists():
            read_type.mkdir()
        read_type_bin = workspace.joinpath(name, "0")
        if not read_type_bin.exists():
            read_type_bin.mkdir()

        for read in os.listdir(directory):
            read_path = directory.joinpath(read)
            read_save = workspace.joinpath(name, "0", read)
            shutil.copy(read_path, read_save)


if __name__ == '__main__':
    unittest.main()

