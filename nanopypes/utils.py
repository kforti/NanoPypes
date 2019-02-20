import os
import shutil
import csv
from pathlib import Path
import json
from abc import ABC, abstractmethod
from nanopypes.objects import BaseCalledData

def temp_dirs(data_dir, temp_location):
    """ Create temp directories and divide input data into these directories
    Return list of temp directory locations
    :Parameters:
    - 'data_dir': string name of the directory
    - 'temp_location': string relative path to where the temp directory is to be located
    """
    temp_location = Path(temp_location)
    data_dir = Path(data_dir)
    temp_path = temp_location.joinpath('temp')
    temp_path.mkdir()

    dir_len = len(os.listdir(str(data_dir)))
    num_splits = int(dir_len / 4)

    if dir_len % num_splits == 0:
        num_files = int(dir_len / num_splits)
    else:
        num_files = int(dir_len / num_splits) + 1

    dirs_list = []
    files = file_generator(data_dir)
    for i in range(num_splits):
        count = 0
        dir_name = str(i)
        p = temp_path.joinpath(dir_name)
        p.mkdir()
        while count < num_files:
            try:
                file_path = next(files)
            except Exception as e:
                print(e)
                break
            file_name = Path(file_path).name
            new_file_path = p.joinpath(file_name)
            shutil.copyfile(str(file_path), str(new_file_path))
            count += 1

        if len(os.listdir(str(p))) > 0:
            dirs_list.append(str(p))
    return dirs_list

def file_generator(dir):
    for file in os.listdir(str(dir)):
        file_path = dir.joinpath(file)
        yield file_path

def remove_temps(path):
    try:
        shutil.rmtree(str(path))
    except Exception as e:
        print(e)

def collapse_save(save_path):
    """ Collapse all the data into the expected output"""
    save_path = Path(save_path)
    batches = os.listdir(str(save_path))

    pipeline = Pipeline(save_path.joinpath("pipeline.log"))
    seq_sum = Summary(save_path.joinpath("sequencing_summary.txt"))
    seq_tel = Telemetry(save_path.joinpath("sequencing_telemetry.js"))
    config = Configuration(save_path.joinpath("configuration.cfg"))
    workspace = Workspace(save_path.joinpath("workspace"))

    for batch in batches:
        batch_path = save_path.joinpath(batch)

        for temp in os.listdir(str(batch_path)):
            temp_path = batch_path.joinpath(temp)

            config.consume(src=temp_path.joinpath("configuration.cfg"))
            pipeline.consume(src=temp_path.joinpath("pipeline.log"))
            seq_sum.consume(src=temp_path.joinpath("sequencing_summary.txt"))
            seq_tel.consume(src=temp_path.joinpath("sequencing_telemetry.js"))
            workspace.consume(src=temp_path.joinpath("workspace"))

    config.combine()
    pipeline.combine()
    seq_tel.combine()
    seq_sum.combine()
    workspace.combine()

    return BaseCalledData(config=config,
                          pipeline=pipeline,
                          summary=seq_sum,
                          telemetry=seq_tel,
                          workspace=workspace)

    #
    #
    # names = ["pass", "fail", "calibration_strands"]
    # save_path = Path(save_path)
    #
    # for i, bin in enumerate(os.listdir(str(save_path))):
    #     bin_path = save_path.joinpath(bin)
    #     if bin_path.is_file():
    #         continue
    #
    #     for child in os.listdir(str(bin_path)):
    #         if child == "sequencing_summary.txt":
    #             sum_path = bin_path.joinpath(child)
    #             new_sum_path = save_path.joinpath(child)
    #             with open(str(sum_path), mode="r") as file:
    #                 csv_reader = csv.reader(file, delimiter="\t")
    #                 row_num = 0
    #                 for row in csv_reader:
    #                     if i != 0 and row_num == 0:
    #                         row_num += 1
    #                         continue
    #                     row_num += 1
    #                     with open(str(new_sum_path), mode="a") as sum_file:
    #                         csv_writer = csv.writer(sum_file, delimiter="\t")
    #                         csv_writer.writerow(row)
    #
    #         elif child == "workspace":
    #             workspace_path = bin_path.joinpath(child)
    #
    #         elif child == "sequencing_telemetry.js":
    #             with open(str(bin_path.joinpath(child)), "r") as file:
    #                 tel_data = json.load(file)
    #             with open(str(save_path.joinpath(child)), "a") as file:
    #                 json.dump(tel_data, file)
    #
    #         elif i == 0 and child == "configuration.cfg":
    #             shutil.copy(str(bin_path.joinpath(child)), str(save_path.joinpath(child)))
    #
    #         elif i == 0 and child == "pipeline.log":
    #             shutil.copy(str(bin_path.joinpath(child)), str(save_path.joinpath(child)))
    #
    #     if i == 0:
    #         new_workspace = save_path.joinpath(workspace_path.name)
    #         os.mkdir(str(new_workspace))
    #
    #         for name in names:
    #             path = new_workspace.joinpath(name)
    #             if not path.exists():
    #                 path.mkdir()
    #
    #     cal_strands = workspace_path.joinpath("calibration_strands", "unclassified", "0")
    #     new_cal_strands = new_workspace.joinpath("calibration_strands", bin)
    #     if not new_cal_strands.exists():
    #         new_cal_strands.mkdir()
    #
    #     pass_reads = workspace_path.joinpath("pass", "unclassified", "0")
    #     new_pass_reads = new_workspace.joinpath("pass", bin)
    #     if not new_pass_reads.exists():
    #         new_pass_reads.mkdir()
    #
    #     fail_reads = workspace_path.joinpath("fail", "unclassified", "0")
    #     new_fail_reads = new_workspace.joinpath("fail", bin)
    #     if not new_fail_reads.exists():
    #         new_fail_reads.mkdir()
    #
    #
    #     dump_reads(cal_strands, new_cal_strands)
    #     dump_reads(pass_reads, new_pass_reads)
    #     dump_reads(fail_reads, new_fail_reads)
    #
    #     shutil.rmtree(str(bin_path))
    # return 0

class AbstractBasecallOutput(ABC):

    def __init__(self, dest):
        self.dest = dest

    @abstractmethod
    def consume(self):
        pass

    @abstractmethod
    def combine(self):
        pass


class Summary(AbstractBasecallOutput):

    def __init__(self, dest):
        self.summary_data = []
        super().__init__(dest)


    def consume(self, src):
        """Read data from a summary file (src) and add it to the combined summary file (dest)."""
        with open(str(src), 'r') as src_file:
            csv_reader = csv.reader(src_file, delimiter='\t')
            for i, line in enumerate(csv_reader):
                if i == 0:
                    continue
                self.summary_data.append(line)

    def create_summary(self):
        pass

    def combine(self):
        with open(self.dest, 'a') as dest_file:
            csv_writer = csv.writer(dest_file, delimiter='\t')
            for row in self.summary_data:
                csv_writer.writerow(row)

class Telemetry(AbstractBasecallOutput):

    def __init__(self, dest):
        self.telemetry = []
        super().__init__(dest)
        # Initiate the seq_tel json file
        with open(str(dest), "w") as file:
            file.write("[]")

    def consume(self, src):
        with open(str(src), "r") as file:
            try:
                self.telemetry.extend(json.load(file))
            except Exception:
                pass

    def combine(self):
        with open(str(self.dest), "a") as file:
            json.dump(self.telemetry, file)

class Configuration(AbstractBasecallOutput):
    def __init__(self, dest):
        self.config_data = []
        super().__init__(dest)

    def consume(self, src):

        with open(str(src), 'r') as config:
            if self.config_data == []:
                self.config_data = [i for i in config]

            elif self.config_data != []:
                for data in self.config_data:
                    if data != next(config):
                        raise ValueError("unexpected value %s found in config file %s" % (val1, str(cfg)))

    def combine(self):
        with open(str(self.dest), 'w') as config:
            for data in self.config_data:
                config.write(data)

class Pipeline(AbstractBasecallOutput):
    def __init__(self, dest):
        self.pipeline_data = []
        super().__init__(dest)

    def consume(self, src):
        with open(str(src), 'r') as pipeline:
            csv_reader = csv.reader(pipeline, delimiter='\t')
            try:
                self.pipeline_data.append(next(csv_reader))
            except StopIteration:
                pass

    def combine(self):
        with open(str(self.dest), 'a') as pipeline:
            csv_writer = csv.writer(pipeline, delimiter='\t')
            for data in self.pipeline_data:
                csv_writer.writerow(data)

class Workspace(AbstractBasecallOutput):
    def __init__(self, dest):
        super().__init__(dest)
        self.read_types = {} # {type_name: {barcodes: [reads]}}

    def consume(self, src):
        for read_type in os.listdir(str(src)):
            path = src.joinpath(read_type)
            self.read_types[read_type] = {}
            for barcode in os.listdir(str(path)):
                reads = []
                barcode_path = path.joinpath(barcode)
                for read in os.listdir(str(barcode_path)):
                    reads.append(barcode_path, read)
                self.read_types[read_type[barcode]] = reads

    def combine(self):
        os.mkdir(self.dest)
        for read_type in self.read_types.keys():
            type_path = self.dest.joinpath(read_type)
            os.mkdir(type_path)
            for barcode in self.read_types[read_type].keys():
                barcode_path = type_path.joinpath(barcode)
                os.mkdir(barcode_path)
                for read in self.read_types[read_type][barcode]:
                    shutil.move(read, str(barcode_path.joinpath(read)))

def dump_reads(src, dest):
    for read in os.listdir(str(src)):
        shutil.copy(str(src.joinpath(read)), str(dest.joinpath(read)))
    return 0

# config = Configuration()
# config.consume("../tests/test_data/basecall_files/configurations/config_17.cfg")
# config.consume("../tests/test_data/basecall_files/configurations/config_25.cfg")
# config.combine("../tests/test_data/basecall_files/configurations/config_combined.cfg")
