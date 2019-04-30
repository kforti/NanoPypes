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
from nanopypes.pipes.basecaller import AlbacoreBasecaller,collapse_data


from distributed import Client, LocalCluster


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
        albacore = Albacore(kit="SQK-LSK109", flowcell="FLO-MIN106", input_path="test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass",
                            save_path="test_data/basecalled_data/results/local_basecall_test", output_format="fastq")
        retrieved_command = albacore.build_basecall_command(Path('./test_data/1'))
        print(retrieved_command)
        expected_command = ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                         "--kit", "SQK-LSK109", "--output_format", "fastq",
                         "--save_path", "test_data/basecalled_data/results/local_basecall_test/1",
                         "--worker_threads", "1", "--input", "test_data/1", "--reads_per_fastq", "1000"]

        #print(retrieved_command, "\n", expected_command)
        self.assertTrue(retrieved_command == expected_command)

    def test_001_albacore_batches(self):
        albacore = Albacore(kit="SQK-LSK109", flowcell="FLO-MIN106",
                            input_path="test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass",
                            save_path="test_data/basecalled_data/results/local_basecall_test", output_format="fastq")
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
        albacore = Albacore(kit="SQK-LSK109", flowcell="FLO-MIN106",
                            input_path="test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass",
                            save_path="test_data/basecalled_data/results/local_basecall_test", output_format="fastq")

        func = albacore.build_func()
        res = func(["echo", "hello"])
        albacore_res = func(["read_fast5_basecaller.py", "--help"])
        print(albacore_res)

########################################################################
### Test Albacore Basecaller                                          ###
########################################################################


class TestBasecallLocal(unittest.TestCase):
    """Tests for the Albacore class."""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""
        data_input_path = Path('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass')
        save_path = Path('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_test')

        shutil.rmtree(str(save_path))
        save_path.mkdir()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_000_basecall_albacore(self):
        """Build a cluster object with yaml"""
        flowcell = 'FLO-MIN106'
        input_path = 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'
        save_path = 'test_data/basecalled_data/results/local_basecall_test'
        kit = 'SQK-LSK109'
        output_format = 'fastq'

        cluster = LocalCluster()
        client = Client(cluster)

        num_workers = 4

        albacore_basecaller(input_path=input_path, save_path=save_path, kit=kit, flowcell=flowcell, expected_workers=num_workers, output_format=output_format, client=client)

    # def test_002_check_basecall(self):
    #     input_reads = []
    #     bc_path = 'test_data/basecalled_data/results/local_basecall_test'
    #     for path, subdirs, files in os.walk('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'):
    #         input_reads.extend(files)
    #
    #     basecalled_reads = []
    #
    #     for path, subdirs, files in os.walk('test_data/basecalled_data/results/local_basecall_test/workspace'):
    #         basecalled_reads.extend(files)
    #
    #     for read in basecalled_reads:
    #         self.assertTrue(read in input_reads)
    #     for read in input_reads:
    #         self.assertTrue(read in basecalled_reads)
    #
    #     self.assertTrue(check_basecall(bc_path, input_reads))

    def test_003_continue_basecall(self):
        pass

class TestBasecallLSFCluster(unittest.TestCase):
    """Test basecaller on lsf cluster"""

    @classmethod
    def setUp(self):
        """Set up test fixtures, if any."""

        data_input_path = Path(
            'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass')
        save_path = Path(
            'test_data/basecalled_data/results/local_basecall_test')
        try:
            shutil.rmtree(str(save_path))
            save_path.mkdir()
        except Exception as e:
            pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_000_basecall_albacore(self):
        """Build a cluster object with yaml"""
        flowcell = 'FLO-MIN106'
        input_path = 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'
        save_path = 'test_data/basecalled_data/results/local_basecall_test'
        kit = 'SQK-LSK109'
        output_format = 'fastq'

        config = Configuration(config="test_configs/remote_builds.yml")
        compute_config = config.get_compute("cluster1")
        cluster = Cluster(compute_config, umass_mem=2480, logs=True)
        scheduler_address = cluster.connect()
        client = Client(scheduler_address)

        num_workers = cluster.expected_workers

        albacore_basecaller(input_path=input_path, save_path=save_path, kit=kit, flowcell=flowcell,
                            expected_workers=num_workers, output_format=output_format, client=client)

    # def test_002_check_basecall(self):
    #     input_reads = []
    #     bc_path = 'test_data/basecalled_data/results/local_basecall_test'
    #     for path, subdirs, files in os.walk(
    #         'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'):
    #         input_reads.extend(files)
    #
    #     basecalled_reads = []
    #
    #     for path, subdirs, files in os.walk('test_data/basecalled_data/results/local_basecall_test/workspace'):
    #         basecalled_reads.extend(files)
    #
    #     for read in basecalled_reads:
    #         self.assertTrue(read in input_reads)
    #     for read in input_reads:
    #         self.assertTrue(read in basecalled_reads)
    #
    #     self.assertTrue(check_basecall(bc_path, input_reads))

    def test_003_continue_basecall(self):
        pass


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

