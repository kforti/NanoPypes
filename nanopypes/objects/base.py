from pathlib import Path
import os
import queue
import math

from ont_fast5_api.fast5_file import Fast5File
from ont_fast5_api.multi_fast5 import MultiFast5File
from ont_fast5_api.fast5_interface import is_multi_read


class ObjectData:
    def __init__(self):
        pass

    @property
    def path(self):
        pass

class FileData(ObjectData):

    def __init__(self, path=None, batch_size=None):
        self._path = path
        self._children = os.listdir(str(self._path))
        self._structure = self._get_structure()
        self._batch_size = batch_size

        self.generator_handle = {'paths_generator': self.get_paths_generator()}

    @property
    def path(self):
        return self._path

    @property
    def structure(self):
        return self._structure
    @property
    def batch_size(self):
        return self._batch_size

    @batch_size.setter
    def batch_size(self, size):
        self._batch_size = size
        return

    @property
    def num_batches(self):
        return math.ceil(len(self._children) / self._batch_size)

    def _get_structure(self):
        files = False
        dirs = False
        path = Path(self.path)

        if self._children == []:
            return None

        for child in self._children:
            child_path = path.joinpath(child)

            if child_path.is_file():
                files = True
            elif child_path.is_dir():
                dirs = True
            if files and dirs:
                return 'mix'

        if files:
            return 'dir_files'
        elif dirs:
            return 'dir_dirs'

    def create_queue(self, generator_handle):
        q = queue.Queue()
        gen = self.generator_handle[generator_handle]
        for batch in gen():
            q.put(batch)
        return q

    def get_paths_generator(self, full_path=False, path_obj=False):
        if full_path:
            path = Path(self._path)
        else:
            path = Path()

        def paths_generator():
            batch = []
            for child in self._children:
                if path_obj:
                    batch.append(path.joinpath(child))
                else:
                    batch.append(str(path.joinpath(child)))
                if len(batch) == self._batch_size:
                    yield batch
                    batch = []
            yield batch

        return paths_generator


class NanoporeSequenceData(FileData):
    def __init__(self, path=None, batch_size=None):
        super().__init__(path=path, batch_size=batch_size)
        if self.structure == 'mix':
            raise IOError("Input data should be a directory of directories or a directory of files")
        self.multi_fast5 = self._is_multi_fast5()

    def _is_multi_fast5(self):
        path = Path(self.path)
        if self.structure == 'dir_dirs':
            for child in self._children:
                path = path.joinpath(child)
                break

        for file in os.listdir(str(path)):
            file_path = path.joinpath(file)
            if file_path.is_dir():
                raise IOError("Input data should be a directory of directories or a directory of files")
            multi = is_multi_read(str(file_path))
            break
        return multi

if __name__ == '__main__':
    # np_data = NanoporeSequenceData(path='/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass',
    #                                batch_size=3)
    # q = np_data.create_queue('paths_generator')
    # for i in range(np_data.num_batches):
    #     print(q.get())
    my_list = [1, 2, 3, 4, 5, 6, 7, 87]
    l = (i for i in my_list)
    print(next(l))
