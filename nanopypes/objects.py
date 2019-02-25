import h5py
import os
from pathlib import Path

class SeqOutput:
    """ Data type for managing and manipulating Raw Fast5 MinIon sequencing data"""
    def __init__(self, input_path):
        self.input_path = input_path

    @property
    def path(self):
        """
        Return the input_path associated with a RawFast5 instance
        """
        return self.input_path

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


class Experiment:
    pass

class Sample:
    def __init__(self, path):
        self._path = None
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
        return self._path

    @property
    def num_bins(self):
        num = len([i for i in range(os.listdir(self._path))])
        return num

class BaseCalledData:
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




