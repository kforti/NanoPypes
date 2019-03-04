import h5py
import os
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
        pass


class Experiment(NanoPypeObject):

    def __init__(self, path):
        super().__init__(path)
        self._samples = os.listdir(str(self.path))

    @property
    def samples(self):
        return self._samples

    def get_sample(self, name):
        return Sample(self.path.joinpath(name))

class Sample(NanoPypeObject):

    @property
    def num_batches(self):
        num = len(os.listdir(self._path))
        return num


class RawRead(NanoPypeObject):

    def __init__(self, path):
        super().__init__(path)

    @property
    def fast5(self):
        return h5py.File(self.path, 'r')

    @property
    def read_name(self):
        return self.fast5.filename

    @property
    def structure(self):
        self.iter_group(self.fast5, 0)

    @property
    def signal(self):
        return self.fast5.get('Signal')

    def iter_group(self, group, layer=0):
        for key in group:
            print("\t" * layer, key)
            if isinstance(group.get(key), h5py.Group):
                self.iter_group(group.get(key), layer + 1)


class _ReadTypes(NanoPypeObject):
    pass

f = RawRead('/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/minion_sample_raw_data/fast5/pass/0/imac_ad_umassmed_edu_20181108_FAK30311_MN27234_sequencing_run_test_61366_read_102_ch_58_strand.fast5')
print(f.signal)
