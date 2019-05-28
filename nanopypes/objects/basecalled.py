import csv
import json
import os
import re
from functools import reduce
from pathlib import Path
from abc import ABC, abstractmethod
import shutil

from ont_fast5_api.fast5_file import Fast5File
from nanopypes.objects.raw import ReadFile
from nanopypes.objects.base import DataObject


class BaseCalledData(DataObject):
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


class ParallelBaseCalledData():
    def __init__(self, path):
        self.path = Path(path)
        self.batches = []
        self.processed_batches = []

        #Create parallel batch objects
        for batch in os.listdir(str(path)):
            if batch == 'workspace':
                continue
            self.batches.append(ParallelBatch(self.path.joinpath(batch),
                                              telemetry=Telemetry(self.path.joinpath("sequencing_telemetry.js")),
                                              summary=SequencingSummary(self.path.joinpath("sequencing_summary.txt")),

                                              pipeline=PipelineLog(self.path.joinpath("pipeline.log")),
                                              configuration=MinIONConfiguration(self.path.joinpath("configuration.cfg"))))

    @property
    def num_batches(self):
        return len(self.batches)


    def add_batches(self, batch1, batch2):
        return batch1 + batch2

    def collapse_parallel_data(self, compute=None):
        print("Collapsing saved data... ")
        if compute:

            batches = compute.map(self._batch_digest, self.batches)
            #compute.show_progress()


            collapsed_batch = reduce(self.add_batches, batches)

            collapsed_batch.combine_data()
            return BaseCalledData(path=self.path,
                                  config=collapsed_batch.configuration,
                                  summary=collapsed_batch.summary,
                                  telemetry=collapsed_batch.telemetry,
                                  workspace=self.path.joinpath('workspace'),
                                  pipeline=collapsed_batch.pipeline)

    def _batch_digest(self, batch):
        batch.digest_splits()
        return batch


class ParallelBatch():
    def __init__(self, path, telemetry, summary, pipeline, configuration):
        self.path = Path(path)
        self._splits = [self.path.joinpath(split) for split in os.listdir(str(self.path))]
        self._telemetry = telemetry
        self._summary = summary
        self._pipeline = pipeline
        self._configuration = configuration

    @property
    def num_splits(self):
        return len(self._splits)

    @property
    def splits(self):
        return self._splits

    @property
    def telemetry(self):
        return self._telemetry

    @property
    def summary(self):
        return self._summary

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def configuration(self):
        return self._configuration

    def combine_data(self):
        self.telemetry.combine()
        self.summary.combine()
        self.pipeline.combine()
        self.configuration.combine()

    def digest_splits(self):
        print("digesting splits... \n Batch number: ", self.path.name)
        for split in self.splits:
            self._configuration.consume(src=split.joinpath("configuration.cfg"))
            self._pipeline.consume(src=split.joinpath("pipeline.log"))
            self._summary.consume(src=split.joinpath("sequencing_summary.txt"))
            self._telemetry.consume(src=split.joinpath("sequencing_telemetry.js"))

    def __add__(self, other):
        print("Adding batch.... ")
        pipeline = self.pipeline + other.pipeline
        summary = self.summary + other.summary
        configuration = self.configuration + other.configuration
        telemetry = self.telemetry + other.telemetry
        return ParallelBatch(path=self.path,
                             telemetry=telemetry,
                             summary=summary,
                             pipeline=pipeline,
                             configuration=configuration)


class BasecalledRead(ReadFile):
    """Basecalled read will have either or both fastq/fast5 asociated with it."""
    pass


class _ReadTypes(DataObject):
    """Read type (calibration_strand, pass, fail) present after basecalling.
    parent => worksapce
    Directory of barcodes or directory of fast5/fastq files"""
    pass


class BaseCalledReadBarcodes(DataObject):
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


class SequencingSummary():

    def __init__(self, dest, data=[]):
        self.header = ['filename', 'read_id', 'run_id', 'channel', 'start_time', 'duration', 'num_events', 'passes_filtering', 'template_start', 'num_events_template', 'template_duration', 'num_called_template', 'sequence_length_template', 'mean_qscore_template', 'strand_score_template', 'calibration_strand_genome_template', 'calibration_strand_identity_template', 'calibration_strand_accuracy_template', 'calibration_strand_speed_bps_template', 'barcode_arrangement', 'barcode_score', 'barcode_full_arrangement', 'front_score', 'rear_score', 'front_begin_index', 'front_foundseq_length', 'rear_end_index', 'rear_foundseq_length', 'kit', 'variant']
        self._summary_data = data
        super().__init__(dest)

    @property
    def summary_data(self):
        return self._summary_data

    def consume(self, src):
        """Read data from a summary file (src) and add it to the combined summary file (dest)."""
        with open(str(src), 'r') as src_file:
            csv_reader = csv.reader(src_file, delimiter='\t')
            for i, line in enumerate(csv_reader):
                if i == 0:
                    continue
                self._summary_data.append(line)

    def combine(self):
        with open(str(self.dest), 'a') as dest_file:
            csv_writer = csv.writer(dest_file, delimiter='\t')
            csv_writer.writerow(self.header)
            for row in self._summary_data:
                csv_writer.writerow(row)

    def __add__(self, other):
        summary_data = self._summary_data + other.summary_data
        return SequencingSummary(dest=self.dest, data=summary_data)


class Telemetry():

    def __init__(self, path):
        self._path = Path(path)
        self._telemetry = self.get_data(path)

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self.get_data(self.path)

    def get_data(self, path):
        data = []
        with open(str(path), 'r') as file:
            for line in file:
                data.append(line)
        file.close()
        return data

    @property
    def data(self):
        return self._telemetry

    def consume(self, src):
        with open(str(src), "r") as file:
            self._telemetry.extend(json.load(file))

    def combine(self):
        if self._telemetry == []:
            raise ValueError("You are trying to write empty data")
        with open(str(self.dest), "a") as file:
            json.dump(self._telemetry, file)

    def __add__(self, other):
        telemetry_data = self._telemetry + other.data
        return Telemetry(dest=self.dest, data=telemetry_data)


class MinIONConfiguration():
    def __init__(self, dest, data=[]):
        self._config_data = data
        super().__init__(dest)

    def consume(self, src):

        with open(str(src), 'r') as config:
            if self._config_data == []:
                self._config_data = [i for i in config]

            elif self._config_data != []:
                for data in self._config_data:
                    if data != next(config):
                        pass
                        # raise ValueError("unexpected value %s found in config file %s" % (val1, str(cfg)))

    def combine(self):
        with open(str(self.dest), 'w') as config:
            for data in self._config_data:
                config.write(data)

    def __add__(self, other):
        config_data = self._config_data + other._config_data
        return MinIONConfiguration(dest=self.dest, data=config_data)

class PipelineLog():
    def __init__(self, dest, data=[], logs=[]):
        self.pipeline_data = data
        self.pipeline_logs = logs
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

    def __add__(self, other):
        pipe_data = self.pipeline_data + other.pipeline_data
        pipe_logs = self.pipeline_logs + other.pipeline_logs
        return PipelineLog(dest=self.dest, data=pipe_data, logs=pipe_logs)


class Workspace():
    def __init__(self, dest):
        super().__init__(dest)

    def consume(self, src):
        for read_type in os.listdir(str(src)):
            path = src.joinpath(read_type)
            for barcode in os.listdir(str(path)):
                self.combine(src, read_type, barcode)

    def combine(self, src_path, read_type, barcode):
        try:
            if not self.dest.exists():
                self.dest.mkdir()
            if not self.dest.joinpath(read_type).exists():
                self.dest.joinpath(read_type).mkdir()
            if not self.dest.joinpath(read_type, barcode).exists():
                self.dest.joinpath(read_type, barcode).mkdir()
        except FileExistsError:
            pass

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



