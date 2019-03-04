import csv
import json
import os
import re
from abc import ABC, abstractmethod
import shutil
from ont_fast5_api.fast5_file import Fast5File
from nanopypes.objects.raw import ReadFile
from nanopypes.objects.base import NanoPypeObject


class BaseCalledData(NanoPypeObject):
    """Data that is returned after basecalling
        Contains:
            Configuration
            Summary
            Telemetry
            Pipeline
            Workspace"""

    def __init__(self, path, config, summary, telemetry, pipeline, workspace):
        self._path = path
        self._config = config
        self._summary = summary
        self._telemetry = telemetry
        self._pipeline = pipeline
        self._workspace = workspace

    @property
    def path(self):
        return self._path

    @property
    def configuration(self):
        return self._config

    @property
    def summary(self):
        return self._summary

    @property
    def telemetry(self):
        return self._telemetry

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def workspace(self):
        return self._workspace


class BasecalledRead(ReadFile):
    """Basecalled read will have either or both fastq/fast5 asociated with it."""
    pass


class _ReadTypes(NanoPypeObject):
    """Read type (calibration_strand, pass, fail) present after basecalling.
    parent => worksapce
    Directory of barcodes or directory of fast5/fastq files"""
    pass


class BaseCalledReadBarcodes(NanoPypeObject):
    """Directory of barcodes
    parent => ReadType (directory labeled either calibration_strand, pass, or fail)"""
    def __init__(self, path):
        super().__init__(path)

    def check_data(self):
        for barcode in self.barcodes:
            search_barcode = re.search(r'([Uu]nclassified)|[0-9]+', barcode)
            if search_barcode:
                #print(barcode, "  PASS")
                continue
            else:
                #print(barcode, "  FAIL")
                raise Warning("Check that your barcodes are correct")

    @property
    def barcodes(self):
        return os.listdir(str(self.path))

    @property
    def num_barcodes(self):
        return len(os.listdir(self.path))


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
                        pass
                        # raise ValueError("unexpected value %s found in config file %s" % (val1, str(cfg)))

    def combine(self):
        with open(str(self.dest), 'w') as config:
            for data in self.config_data:
                config.write(data)


class PipelineLog(AbstractBasecallOutput):
    def __init__(self, dest):
        self.pipeline_data = []
        self.pipeline_logs = []
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

    def consume(self, src):
        for read_type in os.listdir(str(src)):
            path = src.joinpath(read_type)
            for barcode in os.listdir(str(path)):
                self.combine(src, read_type, barcode)

    def combine(self, src_path, read_type, barcode):

        if not self.dest.exists():
            self.dest.mkdir()
        if not self.dest.joinpath(read_type).exists():
            self.dest.joinpath(read_type).mkdir()
        if not self.dest.joinpath(read_type, barcode).exists():
            self.dest.joinpath(read_type, barcode).mkdir()

        #dump reads from barcode dir or batch within barcode dir
        for child in os.listdir(str(src_path.joinpath(read_type, barcode))):
            if src_path.joinpath(read_type, barcode, child).is_file():
                self.dump_reads(src_path.joinpath(read_type, barcode), self.dest.joinpath(read_type, barcode))

            if src_path.joinpath(read_type, barcode, child).is_dir():
                self.dump_reads(src_path.joinpath(read_type, barcode, child), self.dest.joinpath(read_type, barcode))

    def dump_reads(self, src, dest):
        for read in os.listdir(str(src)):
            shutil.copy(str(src.joinpath(read)), str(dest.joinpath(read)))
        return 0
