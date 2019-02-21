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

    return BaseCalledData(config=config,
                          pipeline=pipeline,
                          summary=seq_sum,
                          telemetry=seq_tel,
                          workspace=workspace)


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
        self.summary_data = [['filename', 'read_id', 'run_id', 'channel', 'start_time', 'duration', 'num_events', 'passes_filtering', 'template_start', 'num_events_template', 'template_duration', 'num_called_template', 'sequence_length_template', 'mean_qscore_template', 'strand_score_template', 'calibration_strand_genome_template', 'calibration_strand_identity_template', 'calibration_strand_accuracy_template', 'calibration_strand_speed_bps_template', 'barcode_arrangement', 'barcode_score', 'barcode_full_arrangement', 'front_score', 'rear_score', 'front_begin_index', 'front_foundseq_length', 'rear_end_index', 'rear_foundseq_length', 'kit', 'variant']]
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
        with open(str(self.dest), 'a') as dest_file:
            csv_writer = csv.writer(dest_file, delimiter='\t')
            for row in self.summary_data:
                csv_writer.writerow(row)


class Telemetry(AbstractBasecallOutput):

    def __init__(self, dest):
        self.telemetry = []
        super().__init__(dest)
        # Initiate the seq_tel json file
        # with open(str(dest), "w") as file:
        #     file.write("[]")

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
            while True:
                try:
                    self.pipeline_data.append(next(csv_reader))
                except StopIteration:
                    break

    def combine(self):
        with open(str(self.dest), 'a') as pipeline:
            csv_writer = csv.writer(pipeline, delimiter='\t')
            for data in self.pipeline_data:
                csv_writer.writerow(data)


class Workspace(AbstractBasecallOutput):
    def __init__(self, dest):
        super().__init__(dest)
        # self.read_types = {} # {type_name: {barcodes: [reads]}}

    def consume(self, src):
        for read_type in os.listdir(str(src)):
            path = src.joinpath(read_type)
            self.read_types[read_type] = {}
            for barcode in os.listdir(str(path)):
                self.combine(path, read_type, barcode)

    def combine(self, src_path, read_type, barcode):
        if not self.dest.exists():
            self.dest.mkdir()
        if not self.dest.joinpath(read_type).exists():
            self.dest.joinpath(read_type).mkdir()
        if not self.dest.joinpath(read_type, barcode).exists():
            self.dest.joinpath(read_type, barcode).mkdir()

        for batch in os.listdir(str(src_path.joinpath(read_type, barcode))):
            for read in os.listdir(str(src_path.joinpath(read_type, barcode, batch))):
                shutil.copy(str(src_path.joinpath(read_type, barcode, batch, read)), str(self.dest.joinpath(read_type, barcode, read)))
        return 0



# config = Configuration()
# config.consume("../tests/test_data/basecall_files/configurations/config_17.cfg")
# config.consume("../tests/test_data/basecall_files/configurations/config_25.cfg")
# config.combine("../tests/test_data/basecall_files/configurations/config_combined.cfg")
