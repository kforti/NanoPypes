#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""

import os
import shutil
import unittest
from pathlib import Path
from click.testing import CliRunner
from nanopypes.albacore import Albacore, Cluster
from nanopypes.cli import parallel_basecaller
from nanopypes.objects import Sample
from nanopypes.nanopypes import basecall
from nanopypes.utils import temp_dirs, remove_temps, collapse_save

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
        save_path = "test_data/basecalled_data/results"
        shutil.copytree(save_path, "test_data/basecalled_data/test_results")

    @classmethod
    def tearDown(self):
        """Tear down test fixtures, if any."""
        shutil.rmtree("test_data/basecalled_data/test_results")

    def test_000_temp_dirs(self):
        """Test the creation of temp dirs and distribution of the data into those dirs."""
        sample_raw_data = "test_data/minion_sample_raw_data/fast5/pass/0"
        reads = os.listdir(sample_raw_data)
        temps = temp_dirs(sample_raw_data, "test_data/minion_sample_raw_data")

        temp_reads = []
        for temp in temps:
            for read in os.listdir(temp):
                temp_reads.append(read)

        for read in reads:
            self.assertTrue(read in temp_reads)

        for read in temp_reads:
            self.assertTrue(read in reads)

    def test_001_remove_temps(self):
        """Remove the temporary directories created in previous test"""
        temp_path = "test_data/minion_sample_raw_data/temp"
        remove_temps(temp_path)
        self.assertTrue(not Path(temp_path).exists())

    def test_002_collapse_save(self):
        """Test the collapsing of parallel basecalled data into the
        data format of normal albacore basecalling for the given input"""

        save_path = Path("test_data/basecalled_data/test_results")
        cal_reads = {}
        pass_reads = {}
        fail_reads = {}
        bins = os.listdir(str(save_path))
        for bin in bins:
            cal_reads[bin] = []
            cal_path = save_path.joinpath(bin, "workspace", "calibration_strands", "0")
            for read in os.listdir(cal_path):
                cal_reads[bin].append(read)

            pass_reads[bin] = []
            pass_path = save_path.joinpath(bin, "workspace", "pass", "0")
            for read in os.listdir(pass_path):
                pass_reads[bin].append(read)

            fail_reads[bin] = []
            fail_path = save_path.joinpath(bin, "workspace", "fail", "0")
            for read in os.listdir(fail_path):
                fail_reads[bin].append(read)

        collapse_save(save_path)
        cal_save = save_path.joinpath("workspace", "calibration_strands")
        pass_save = save_path.joinpath("workspace", "pass")
        fail_save = save_path.joinpath("workspace", "fail")
        for bin in bins:
            save_cal_reads = os.listdir(cal_save.joinpath(bin))
            for read in save_cal_reads:
                self.assertTrue(read in cal_reads[bin])
            for read in cal_reads[bin]:
                self.assertTrue(read in save_cal_reads)

            save_pass_reads = os.listdir(pass_save.joinpath(bin))
            for read in save_pass_reads:
                self.assertTrue(read in pass_reads[bin])
            for read in pass_reads[bin]:
                self.assertTrue(read in save_pass_reads)

            save_fail_reads = os.listdir(fail_save.joinpath(bin))
            for read in save_fail_reads:
                self.assertTrue(read in fail_reads[bin])
            for read in fail_reads[bin]:
                self.assertTrue(read in save_fail_reads)


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

        self.assertTrue(["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fast5",
                        "--save_path", "./test_data/basecalled_data/results/0", "--worker_threads", "1", "--input", "./test_data/", "--barcoding"] == command)

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

        self.assertTrue(
            ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fast5",
             "--save_path", "./test_data/basecalled_data/results/0", "--worker_threads", "1", "--input", "./test_data/",
             "--barcoding"] == command)

    def test_002_albacore_commands(self):
        """Test the albacore commands that are generated from passing both yaml and custom input."""
        yaml = "build_command_test.yml"
        albacore = Albacore(input=yaml, save_path="/project/umw_athma_pai/kevin/data", barcoding=False, output_format="fastq")
        command = albacore.build_command('./test_data/', '0')

        self.assertTrue(
            ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fastq",
             "--save_path", "/project/umw_athma_pai/kevin/data/0", "--worker_threads", "1", "--input", "./test_data/",
             "--reads_per_fastq", "1000"] == command)

    def test_003_albacore_build_func(self):
        """Test the function that is built from albacore."""
        sample = Sample('test_data/minion_sample_raw_data/fast5/pass')
        save_path = './test_data/basecalled_data/results'
        albacore = Albacore(input=sample,
                            flowcell='FLO-MIN106',
                            kit='SQK-LSK109',
                            save_path=save_path,
                            output_format='fast5',
                            barcoding=True,
                            )
        func = albacore.build_func()
        res = func(["echo", "hello"])
        albacore_res = func(["read_fast5_basecaller.py", "--help"])

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


# class TestCluster(unittest.TestCase):
#     """Tests for the Albacore class."""
#
#     @classmethod
#     def setUp(self):
#         """Set up test fixtures, if any."""
#         from nanopypes.albacore import Albacore
#
#     def tearDown(self):
#         """Tear down test fixtures, if any."""
#
#     def test_000_add_workers(self):
#         """Build a cluster object and add workers"""
#         add_workers = 100
#         cluster = Cluster(config="build_command_test.yml")
#         num_workers = cluster.num_workers
#         expected_workers = add_workers + num_workers
#         cluster.add_workers()


########################################################################
### Test Helper Functions                                                 ###
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

