#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pai-nanopypes` package."""

import os
import shutil
import unittest
import json
import csv
import re
from pathlib import Path
from nanopypes.config import Configuration
from nanopypes.oxnano import Albacore
from nanopypes.compute import Cluster
from nanopypes.objects.basecalled import ParallelBaseCalledData

from nanopypes.run_pipes import albacore_basecaller
from nanopypes.pipes.basecaller import AlbacoreBasecaller



########################################################################
### Test Albacore                                                    ###
########################################################################
class TestAlbacoreLocal(unittest.TestCase):
    """Tests for the Albacore class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_albacore_commands(self):
        """Test the albacore commands that are generated from passing custom inputs."""
        config = Configuration("test_configs/local_builds.yml")
        albacore = Albacore(config=config)
        retrieved_command = albacore.build_basecall_command('./test_data/1', '0')
        expected_command = ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                         "--kit", "SQK-LSK109", "--output_format", "fast5",
                         "--save_path", "test_data/basecalled_data/results/local_basecall_test/0/1",
                         "--worker_threads", "1", "--input", "./test_data/1", "--barcoding"]

        #print(retrieved_command, "\n", expected_command)
        self.assertTrue(retrieved_command == expected_command)

    def test_001_albacore_batches(self):
        config = Configuration("test_configs/local_builds.yml")
        albacore = Albacore(config=config)
        expected_batches = [Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/0'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/1'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/2'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/3'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/4'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/5'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/6'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/7'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/8'),
                            Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/9')]

        actual_batches = albacore.batches_for_basecalling

        #print("BATCHES....... ", expected_batches, "\n", actual_batches)
        for batch in expected_batches:
            self.assertTrue(batch in actual_batches)
        for batch in actual_batches:
            self.assertTrue(batch in expected_batches)

    def test_003_albacore_build_func(self):
        """Test the function that is built from albacore."""
        config = Configuration("test_configs/local_builds.yml")
        albacore = Albacore(config=config)

        func = albacore.build_func()
        res = func(["echo", "hello"])
        albacore_res = func(["read_fast5_basecaller.py", "--help"])
        print(albacore_res)


class TestAlbacoreRemote(unittest.TestCase):
    """Tests for the Albacore class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_albacore_commands(self):
        """Test the albacore commands that are generated from passing custom inputs."""
        config = Configuration("test_configs/remote_builds.yml")
        albacore = Albacore(config=config)
        retrieved_command = albacore.build_basecall_command('./test_data/1', '0')
        expected_command = ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                            "--kit", "SQK-LSK109", "--output_format", "fast5",
                            "--save_path", "test_data/basecalled_data/results/0/1",
                            "--worker_threads", "1", "--input", "./test_data/1"]
        # print(retrieved_command, "\n", expected_command)
        self.assertTrue(retrieved_command == expected_command)

    # def test_001_albacore_commands(self):
    #     """Test the albacore commands that are generated from passing yaml input."""
    #     yaml = "test_configs/local_builds.yml"
    #     albacore = Albacore(input=yaml)
    #     command = albacore.build_command('./test_data/1', '0')
    #     print(command)
    #     self.assertTrue(
    #         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fast5",
    #          "--save_path", "./test_data/basecalled_data/results/0/1", "--worker_threads", "1", "--input", "./test_data/1"] == command)

    # def test_002_albacore_commands(self):
    #     """Test the albacore commands that are generated from passing both yaml and custom input."""
    #     yaml = "test_configs/local_builds.yml"
    #     albacore = Albacore(input=yaml, save_path="/project/umw_athma_pai/kevin/data", barcoding=False, output_format="fastq")
    #     command = albacore.build_command('./test_data/1', '0')
    #
    #     self.assertTrue(
    #         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106", "--kit", "SQK-LSK109", "--output_format", "fastq",
    #          "--save_path", "/project/umw_athma_pai/kevin/data/0/1", "--worker_threads", "1", "--input", "./test_data/1",
    #          "--reads_per_fastq", "1000"] == command)

    def test_003_albacore_build_func(self):
        """Test the function that is built from albacore."""
        config = Configuration("test_configs/remote_builds.yml")
        albacore = Albacore(config=config)

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
### Test Albacore Basecaller                                          ###
########################################################################


class TestBasecallLocal(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""

        pass

        data_input_path = Path('/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass')
        save_path = Path('/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/basecalled_data/results/local_basecall_test')
        batches = [data_input_path.joinpath(batch) for batch in os.listdir(str(data_input_path))]
        for batch in batches:
            try:
                shutil.rmtree(str(batch.joinpath('split_data')))
            except Exception as e:
                pass
        shutil.rmtree(str(save_path))
        save_path.mkdir()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_000_basecall_albacore(self):
        """Build a cluster object with yaml"""

        config = "test_configs/local_basecall.yml"

        config = Configuration(config)
        compute_configs = config.compute
        compute = Cluster(compute_configs[0])
        albacore = Albacore(config)
        client = compute.connect()
        basecall = AlbacoreBasecaller(albacore=albacore, client=client, max_batch_size=compute.workers)

        basecall()

    def test_001_basecall_albacore(self):
        config = "test_configs/local_basecall.yml"

        config = Configuration(config)
        compute_configs = config.compute
        compute = Cluster(compute_configs[0])
        client = compute.connect()
        albacore = Albacore(config)

        basecall = AlbacoreBasecaller(albacore=albacore, client=client, num_splits=4,
                                      batch_bunch_size=5, continue_on=False)
        basecall.collapse_data()
    # def test_000_basecall_albacore(self):
    #     """Build a cluster object with yaml"""
    #     config = Configuration("test_configs/local_basecall.yml")
    #     compute_configs = config.compute
    #     compute = Cluster(compute_configs[0])
    #     compute.connect()
    #     albacore = Albacore(config)
    #     save_path = albacore.save_path
    #     input_data = albacore.input_path
    #     input_reads = []
    #
    #     if save_path.exists():
    #         shutil.rmtree(str(save_path))
    #     for path, subdirs, files in os.walk(str(input_data)):
    #         input_reads.extend(files)
    #
    #     basecaller = AlbacoreBasecall(albacore, compute, data_splits=4)
    #     basecalled_data = basecaller()
    #     compute.close()


    def test_001_check_basecall(self):
        input_reads = []
        bc_path = 'test_data/basecalled_data/results/local_basecall_test'
        for path, subdirs, files in os.walk('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'):
            input_reads.extend(files)

        basecalled_reads = []

        for path, subdirs, files in os.walk('test_data/basecalled_data/results/local_basecall_test/workspace'):
            basecalled_reads.extend(files)

        for read in basecalled_reads:
            self.assertTrue(read in input_reads)
        for read in input_reads:
            self.assertTrue(read in basecalled_reads)

        self.assertTrue(check_basecall(bc_path, input_reads))

    def test_002_remove_parallel_data(self):
        config = Configuration("test_configs/local_basecall.yml")
        compute_configs = config.compute
        compute = Cluster(compute_configs[0])
        compute.connect()
        albacore = Albacore(config)
        basecaller = AlbacoreBasecall(albacore, compute, data_splits=4)
        basecaller.remove_parallel_data()

    def test_003_continue_basecall(self):
        config = Configuration("test_configs/local_basecall.yml")
        compute_configs = config.compute
        compute = Cluster(compute_configs[0])
        compute.connect()
        albacore = Albacore(config,
                            input='test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass',
                            continue_on=True,
                            save_path='test_data/basecalled_data/results/continue_basecall_local')

        basecaller = AlbacoreBasecall(albacore, compute, data_splits=4)
        basecalled_data = basecaller()
        compute.close()

class TestBasecallRemote(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass


    def test_000_basecall_albacore(self):
        """Build a cluster object with yaml"""
        config = Configuration("test_configs/remote_basecall.yml")
        compute_configs = config.compute
        compute = Cluster(compute_configs[0])
        compute.connect()
        albacore = Albacore(config)
        save_path = albacore.save_path
        input_data = albacore.input_path
        input_reads = []

        shutil.rmtree(str(save_path))
        for path, subdirs, files in os.walk(str(input_data)):
            input_reads.extend(files)

        basecaller = AlbacoreBasecall(albacore, compute, data_splits=100)
        basecalled_data = basecaller()
        compute.close()

        # self.assertTrue(check_basecall(basecalled_data, input_reads))

    def test_001_check_basecall(self):
        input_reads = []
        bc_path = 'test_data/basecalled_data/results/local_basecall_test'
        for path, subdirs, files in os.walk('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'):
            input_reads.extend(files)

        self.assertTrue(check_basecall(bc_path, input_reads))

    def test_002_remove_parallel_data(self):
        config = Configuration("test_configs/remote_basecall.yml")
        compute_configs = config.compute
        compute = Cluster(compute_configs[0])
        compute.connect()
        albacore = Albacore(config)
        basecaller = AlbacoreBasecall(albacore, compute, data_splits=100)
        basecaller.remove_parallel_data()

########################################################################
### Helper Functions                                                 ###
########################################################################

def check_pipeline_log(log, combined_log):
    with open(str(log), "r") as file:
        with open(str(combined_log), "r") as cfile:
            log_data = csv.reader(file, delimiter="\t")
            clog_data = csv.reader(cfile, delimiter="\t")
            clog_rows = list(clog_data)
            #print("CLOGROWS!!!!!!!!!!!!!!!!!!!!!",clog_rows)
            try:
                while True:
                    log_row = next(log_data)
                    if log_row in clog_rows:
                        continue
                    else:
                        print("[PIPELINE]\n", log, "\n", log_row)

                    # clog_row = next(clog_data)
                    # if clog_row == log_row:
                    #     while True:
                    #         val1 = next(log_data)
                    #         val2 = next(clog_data)
                    #         if val1 != val2:
                    #             print("[PIPELINE]\n", val1, '\n', val2, '\n', log)
                    #             # raise ValueError("unexpected value %s found in log file %s. clog shows %s" % (val1, str(log), val2))
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
            #print("COMBINED DATA........ ", combined_data)
            for i, row in enumerate(data):
                if i == 0:
                    continue
                elif row not in combined_data:
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

def check_basecall(bc_data_path, input_reads):

    ## Check reads
    bc_data_path = Path(bc_data_path)
    bc_reads = []
    for path, subdirs, files in os.walk(str(bc_data_path.joinpath('workspace'))):
        bc_reads.extend(files)

    for read in bc_reads:
        if read not in input_reads:
            return False

    for read in input_reads:
        if read not in bc_reads:
            return False

    #Iterate through parallel basecall files
    combined_workspace = bc_data_path.joinpath("workspace")
    combined_sum = bc_data_path.joinpath("sequencing_summary.txt")
    combined_tel = bc_data_path.joinpath("sequencing_telemetry.js")
    combined_pipe = bc_data_path.joinpath("pipeline.log")
    combined_config = bc_data_path.joinpath("configuration.cfg")

    batch_pattern = r'(^)[0-9]+($)'
    for batch in os.listdir(str(bc_data_path)):
        if re.match(batch_pattern, batch):
            for split in os.listdir(str(bc_data_path.joinpath(batch))):
                check_configuration_cfg(bc_data_path.joinpath(batch, split, "configuration.cfg"), combined_config)
                check_seq_sum(bc_data_path.joinpath(batch, split, "sequencing_summary.txt"), combined_sum)
                check_seq_tel(bc_data_path.joinpath(batch, split, "sequencing_telemetry.js"), combined_tel)
                check_pipeline_log(bc_data_path.joinpath(batch, split, "pipeline.log"), combined_pipe)

    return True


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


