import h5py
import os
from pathlib import Path

class NanoPypeObject:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

class SeqOutput(NanoPypeObject):
    """ Data type for managing and manipulating Raw Fast5 MinIon sequencing data"""

    #pass_reads and fail_reads might need to be updated to get read batches
    @property
    def experiments(self):
        experiments = [experiment for experiment in os.listdir(self.input_path)]
        return experiments

    @property
    def samples(self):
        sample_dict = {}
        for experiment in os.listdir(self.input_path):
            sample_dict[experiment] = [sample for sample in os.listdir(self.input_path + '/' + experiment)]
        return sample_dict

    def check_experiment(self, experiment):
        if experiment in self.experiments:
            return True
        else:
            return False

    def check_sample(self, sample):
        samples = self.samples
        for key in samples:
            if sample in samples[key]:
                return True
        return False

    def get_experiment(self, experiment):
        pass

    def get_sample(self, experiment, sample):
        pass


class Experiment(NanoPypeObject):

    def __init__(self):
        super

    @property
    def samples(self):
        return self._samples

class Sample(NanoPypeObject):

    @property
    def num_batches(self):
        num = len(os.listdir(self._path))
        return num


class BaseCalledData(NanoPypeObject):
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


class BasecalledRead(NanoPypeObject):
    pass


