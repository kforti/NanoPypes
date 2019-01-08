import h5py
import os
from pathlib import Path

class RawData:
    """ Data type for managing and manipulating Raw Fast5 MinIon sequencing data"""
    def __init__(self, input_path):
        self.input_path = input_path
        self.pass_reads = self._pass_reads
        self.fail_reads = self._fail_reads

    @property
    def path(self):
        """
        Return the input_path associated with a RawFast5 instance
        """
        return self.input_path

    #pass_reads and fail_reads might need to be updated to get read batches
    @property
    def _pass_reads(self):
        pass
    @property
    def _fail_reads(self):
        pass

    @property
    def num_dirs(self):
        return len([i for i in os.listdir(self.input_path) if i != 'temp'])

    @property
    def storage_type(self):
        """
        Return the storage type as either a directory of directories 'dir_dir' or a directory of files 'dir_file
        '"""
        contents_list = []
        counter = 0
        path = Path(self.input_path)
        for obj in os.listdir(self.input_path):
            if obj == '.DS_Store':
                continue
            i = path.joinpath(obj)
            if i.is_dir():
                contents_list.append(True)
            elif i.is_file():
                contents_list.append(False)
            counter += 1
            if counter == 10:
                break
        if True in contents_list:
            return 'dir_dir'
        else:
            return 'dir_file'

    @property
    def structure(self):
        file = os.listdir(self.input_path)[0]
        self._print_keys(file)

    @property
    def num_reads(self):
        """
        Return the number of reads contained in an input_path
        """
        if self.storage_type == 'dir_dir':
            reads_count = 0
            for dir in os.listdir(self.input_path):
                if dir == '.DS_Store':
                    continue
                reads_dir = self.input_path.joinpath(dir)
                reads_count += self._count_reads(reads_dir)
        elif self.storage_type == 'dir_file':
            reads_count = self._count_reads(self.input_path)

        return reads_count

    def _count_reads(self, reads_dir):
        """Private method used to count reads (files) in a directory"""
        reads_count = 0
        for read in os.listdir(str(reads_dir)):
            if read == '.DS_Store':
                continue
            reads_count += 1
        return reads_count

    def _print_keys(self, x, depth=0):
        keys = []

        try:
            for key in x.keys():
                new_depth = depth + 1
                print(('\t' * depth), key)
                keys.append(key)
                print_keys(x[key], new_depth)
            return keys
        except Exception:
            pass

