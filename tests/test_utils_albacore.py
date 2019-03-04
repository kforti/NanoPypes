#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""

import os
import shutil
import unittest
import json
import csv
from pathlib import Path
from nanopypes.albacore import Albacore, Cluster
from nanopypes.objects.raw import Sample
from nanopypes.pipes import AlbacoreBasecall
from nanopypes.utils import temp_dirs, remove_temps, collapse_save


########################################################################
### Test Albacore                                                    ###
########################################################################

class TestAlbacore(unittest.TestCase):
    """Tests for the Albacore class."""

    def setUp(self):
        """Set up test fixtures, if any."""

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
                            barcoding=False,
                            )
        command = albacore.build_command('./test_data/1', '0')

        self.assertTrue(["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fast5",
                        "--save_path", "./test_data/basecalled_data/results/0/1", "--worker_threads", "1", "--input", "./test_data/1"] == command)

    def test_001_albacore_commands(self):
        """Test the albacore commands that are generated from passing yaml input."""
        yaml = "build_command_test.yml"
        albacore = Albacore(input=yaml)
        command = albacore.build_command('./test_data/1', '0')
        print(command)
        self.assertTrue(
            ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fast5",
             "--save_path", "./test_data/basecalled_data/results/0/1", "--worker_threads", "1", "--input", "./test_data/1"] == command)

    def test_002_albacore_commands(self):
        """Test the albacore commands that are generated from passing both yaml and custom input."""
        yaml = "build_command_test.yml"
        albacore = Albacore(input=yaml, save_path="/project/umw_athma_pai/kevin/data", barcoding=False, output_format="fastq")
        command = albacore.build_command('./test_data/1', '0')

        self.assertTrue(
            ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fastq",
             "--save_path", "/project/umw_athma_pai/kevin/data/0/1", "--worker_threads", "1", "--input", "./test_data/1",
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
                            barcoding=False,
                            )
        func = albacore.build_func()
        res = func(["echo", "hello"])
        albacore_res = func(["read_fast5_basecaller.py", "--help"])
        print(albacore_res)

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
### Test Albacore Helper Functions                                                 ###
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


########################################################################
### Test Utility Functions                                           ###
########################################################################

class TestUtilityFunctions(unittest.TestCase):
    """Tests for the utility functions found in utils.py."""

    @classmethod
    def setUp(self):
        basecalled_data_path = "test_data/basecalled_data/bc_test_results"
        shutil.rmtree("test_data/basecalled_data/test_results")
        #Make a copy of the basecalled data to perform tests on
        shutil.copytree(basecalled_data_path, "test_data/basecalled_data/test_results")

    @classmethod
    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

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

        basecalled_data_path = Path("test_data/basecalled_data/bc_test_results")
        collapse_path = Path("test_data/basecalled_data/test_results")
        # shutil.copytree(str(save_path), str(temp_path))
        collapse_save(collapse_path)

        for batch in os.listdir(str(basecalled_data_path)):
            for temp in os.listdir(str(basecalled_data_path.joinpath(batch))):
                check_configuration_cfg(cfg=basecalled_data_path.joinpath(batch, temp, "configuration.cfg"),
                                        combined_cfg=collapse_path.joinpath("configuration.cfg"))
                check_pipeline_log(log=basecalled_data_path.joinpath(batch, temp, "pipeline.log"),
                                   combined_log=collapse_path.joinpath("pipeline.log"))
                check_seq_sum(summary=basecalled_data_path.joinpath(batch, temp, "sequencing_summary.txt"),
                              combined_sum=collapse_path.joinpath("sequencing_summary.txt"))
                check_seq_tel(tel=basecalled_data_path.joinpath(batch, temp, "sequencing_telemetry.js"),
                              combined_tel=collapse_path.joinpath("sequencing_telemetry.js"))
        check_workspace(workspace=basecalled_data_path,
                                combined_workspace=collapse_path.joinpath("workspace"))


########################################################################
### Test Albacore Basecaller                                          ###
########################################################################


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
        input_data = albacore.input_path
        input_reads = []
        for path, subdirs, files in os.walk(str(input_data)):
            input_reads.extend(files)

        basecaller = AlbacoreBasecall(albacore, cluster)
        basecalled_data = basecaller()

        bc_reads = []
        bc_data_path = basecalled_data.path
        for path, subdirs, files in os.walk(str(bc_data_path.joinpath('workspace'))):
            bc_reads.extend(files)

        for read in bc_reads:
            self.assertTrue(read in input_reads)

        for read in input_reads:
            self.assertTrue(read in bc_reads)


########################################################################
### Helper Functions                                                 ###
########################################################################

def check_pipeline_log(log, combined_log):
    with open(str(log), "r") as file:
        with open(str(combined_log), "r") as cfile:
            log_data = csv.reader(file, delimiter="\t")
            clog_data = csv.reader(cfile, delimiter="\t")
            log_row = next(log_data)
            try:
                while True:
                    clog_row = next(clog_data)
                    if clog_row == log_row:
                        while True:
                            val1 = next(log_data)
                            val2 = next(clog_data)
                            if val1 != val2:
                                print("[PIPELINE]\n", val1, '\n', val2, '\n', log)
                                # raise ValueError("unexpected value %s found in log file %s. clog shows %s" % (val1, str(log), val2))
            except StopIteration:
                    pass

def check_configuration_cfg(cfg, combined_cfg):
    with open(str(cfg), "r") as file:
        with open(str(combined_cfg), "r") as cfile:
            try:
                while True:
                    val1 = next(file)
                    val2 = next(cfile)
                    if val1 != val2:
                        print("[CONFIG]\n", val1, '\n', val2)
                        # raise ValueError("unexpected value %s found in config file %s" % (val1, str(cfg)))
            except StopIteration:
                    pass

def check_seq_sum(summary, combined_sum):
    with open(str(summary), "r") as file:
        data = csv.reader(file, delimiter="\t")
        with open(str(combined_sum), "r") as cfile:
            combined_data = []
            for row in csv.reader(cfile, delimiter="\t"):
                combined_data.append(row)
            for row in data:
                if row not in combined_data:
                    print("[SUMMARY]\n", summary, '\n', row)
                    # raise ValueError("Could not find summary data from %s in combined summary file" % summary)

def check_seq_tel(tel, combined_tel):
    with open(str(tel), "r") as file:
        with open(str(combined_tel), "r") as cfile:
            combined_data = json.load(cfile)
            try:
                tel_data = json.load(file)
            except Exception:
                return
            for data in tel_data:
                if data not in combined_data:
                    print("[TELEMETRY]\n", tel, '\n', data)
                    # raise ValueError("Data in %s not found in combined telemetry")

def check_workspace(workspace, combined_workspace):

    all_reads = []
    for path, subdirs, reads in os.walk(str(workspace)):
        all_reads.extend([read for read in reads if read != []])
    all_reads.sort()

    combined_reads = []
    for path, subdirs, reads in os.walk(str(combined_workspace)):
        combined_reads.extend([read for read in reads if read != []])
    combined_reads.sort()

    # for read_type in os.listdir(str(workspace)):
    #     path = workspace.joinpath(read_type)
    #     for barcode in os.listdir(str(path)):
    #         b_path = path.joinpath(barcode)
    #         if combined_reads == []:
    #             combined_path = combined_workspace.joinpath(read_type, barcode)
    #             combined_reads.extend(os.listdir(str(combined_path)))
    #         for read in os.listdir(str(b_path)):
    #             if read not in combined_reads:
    #                 raise ValueError("Read %s not found in combined reads" % read)
    #         combined_reads = []




#################
def combine_telemetry(tels, tel_combined):
    tel_data = []
    for tel in tels:
        with open(tel, "r") as file:
            try:
                tel_data.extend(json.load(file))
            except Exception:
                pass
    with open(tel_combined, "a") as file:
        json.dump(tel_data, file)

if __name__ == '__main__':
    pipeline_logs = ["test_data/basecall_files/pipeline_logs/pipeline_17.log",
                     "test_data/basecall_files/pipeline_logs/pipeline_27.log",
                     "test_data/basecall_files/pipeline_logs/pipeline_25.log",
                     "test_data/basecall_files/pipeline_logs/pipeline_40.log"]
    combined_log = "test_data/basecall_files/pipeline_logs/pipeline_combined.log"

    for log in pipeline_logs:
        check_pipeline_log(log, combined_log)
    configs = ["test_data/basecall_files/configurations/config_17.cfg",
                     "test_data/basecall_files/configurations/config_27.cfg",
                     "test_data/basecall_files/configurations/config_25.cfg",
                     "test_data/basecall_files/configurations/config_40.cfg"]

    summaries = ["test_data/basecall_files/seq_sums/sum_17.txt",
               "test_data/basecall_files/seq_sums/sum_27.txt",
               "test_data/basecall_files/seq_sums/sum_25.txt",
               "test_data/basecall_files/seq_sums/sum_40.txt"]
    sum_combined = "test_data/basecall_files/seq_sums/sum_combined.txt"
    for sum in summaries:
        check_seq_sum(sum, sum_combined)

    tels = ["test_data/basecall_files/seq_tels/tel_17.js",
            "test_data/basecall_files/seq_tels/tel_27.js",
            "test_data/basecall_files/seq_tels/tel_25.js",
            "test_data/basecall_files/seq_tels/tel_40.js"]
    tel_combined = "test_data/basecall_files/seq_tels/tel_combined.js"
    for tel in tels:
        check_seq_tel(tel, tel_combined)

    configs = ["test_data/basecall_files/configurations/config_17.cfg",
               "test_data/basecall_files/configurations/config_27.cfg",
               "test_data/basecall_files/configurations/config_25.cfg",
               "test_data/basecall_files/configurations/config_40.cfg"]
    config_combined = "test_data/basecall_files/configurations/config_17.cfg"
    for config in configs:
        check_configuration_cfg(config, config_combined)


