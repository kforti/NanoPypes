import h5py
import os
from ont_fast5_api.fast5_interface import is_multi_read
from ont_fast5_api.fast5_read import Fast5Read
from ont_fast5_api.fast5_file import Fast5File
from nanopypes.objects.base import NanoPypeObject

class SeqOutput(NanoPypeObject):
    """ Data type for managing and manipulating Raw Fast5 MinIon sequencing data"""

    #pass_reads and fail_reads might need to be updated to get read batches
    @property
    def experiments(self):
        return os.listdir(self.input_path)

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
        sample_path = self.path.joinpath(experiment, sample)
        return Sample(sample_path)


class Experiment(NanoPypeObject):

    def __init__(self, path):
        super().__init__(path)

    @property
    def samples(self):
        return os.listdir(str(self.path))

    def get_sample(self, name):
        return Sample(self.path.joinpath(name))


class Sample(NanoPypeObject):

    def __init__(self, path):
        super().__init__(path)

    @property
    def pass_batches(self):
        batch_path = self.path.joinpath('fast5', 'pass')
        return [batch_path.joinpath(i) for i in sorted(os.listdir(str(batch_path)))]

    @property
    def fail_batches(self):
        batch_path = self.path.joinpath('fast5', 'fail')
        return [batch_path.joinpath(i) for i in sorted(os.listdir(str(batch_path)))]

    @property
    def num_batches(self):
        """Number of batches in the Sample's fast5 directory"""
        num = len(os.listdir(str(self.path.joinpath('fast5'))))
        return num

    @property
    def read_types(self):
        pass

    @property
    def info(self):
        pass

    @property
    def num_reads(self):
        pass_reads = 0
        fail_reads = 0

        for batch in self.pass_batches:
            pass_reads += len(os.listdir(batch))

        for batch in self.fail_batches:
            fail_reads += len(os.listdir(batch))

        return {'pass': pass_reads, 'fail': fail_reads}


class Fast5Read(Fast5Read):

    def __init__(self, path, read_id):
        super().__init__(path, read_id)

    @property
    def open(self):
        return h5py.File(self.path, 'r')

    @property
    def read_name(self):
        return self.open.filename

    @property
    def contents(self):
        self.iter_group(self.open, 0)

    @property
    def signal(self):
        return self.open.get('Signal')

    def iter_group(self, group, layer=0):
        for key in group:
            print("\t" * layer, key)
            if isinstance(group.get(key), h5py.Group):
                self.iter_group(group.get(key), layer + 1)


class ReadFile(Fast5File):
    pass