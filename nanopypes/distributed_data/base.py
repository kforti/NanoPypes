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
        self._batch_size = batch_size

        self._get_structure()

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
                self._structure = 'mix'
                return

        if files:
            self._structure = 'dir_files'
        elif dirs:
            self._structure = 'dir_dirs'

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

    def __iter__(self):
        pass

from multiprocessing import Pool, cpu_count
import shutil


def move_chunk(chunk, dest):
    dest_path = Path(dest)
    if dest_path.exists() is False:
        dest_path.mkdir()
    for file in chunk:
        shutil.move(file, dest_path.joinpath(Path(file).name))

class NanoporeSequenceData(FileData):
    def __init__(self, path=None, batch_size=None, files_per_dir=4000):
        super().__init__(path=path, batch_size=batch_size)
        if self.structure == 'mix':
            raise IOError("Input data should be a directory of directories or a directory of files")
        self.multi_fast5 = self._is_multi_fast5()
        self.pool = Pool(processes=cpu_count())
        self.files_per_dir = files_per_dir
        self.batch_paths = []

    def _is_multi_fast5(self):
        path = Path(self.path)
        if self.structure == 'dir_dirs':
            path = path.joinpath(self._children[0])

        for file in os.listdir(str(path)):
            file_path = path.joinpath(file)
            if file_path.is_dir():
                raise IOError("Input data should be a directory of directories or a directory of files")
            multi = is_multi_read(str(file_path))
            break
        return multi

    def _structure_data(self):
        if self._structure == 'dir_files' and self.multi_fast5 is False:
            file_chunks = self.file_chunker()
            for i, chunk in enumerate(file_chunks):
                batch_path = Path(self._path).joinpath("batch_{}".format(i))
                self.batch_paths.append(batch_path)
                self.pool.apply(move_chunk, [chunk, batch_path])
        elif self._structure == 'dir_dirs':
            self.batch_paths = [Path(self._path).joinpath(directory) for directory in self._children]

    def file_chunker(self):
        current_chunk = []
        all_chunks = []
        for file in self._children:
            current_chunk.append(Path(self._path).joinpath(file))
            if len(current_chunk) == self.files_per_dir:
                all_chunks.append(current_chunk)
                current_chunk = []
        if current_chunk != []:
            all_chunks.append(current_chunk)

        return all_chunks

    def __iter__(self):
        self._structure_data()
        for batch in self.batch_paths:
            yield batch


if __name__ == '__main__':
    # np_data = NanoporeSequenceData(path='/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass',
    #                                batch_size=3)
    # q = np_data.create_queue('paths_generator')
    # for i in range(np_data.num_batches):
    #     print(q.get())
    input_path = Path("/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/1")
    # for child in os.listdir(input_path):
    #     child_path = input_path.joinpath(child)
    #     if child_path.is_dir():
    #         for file in os.listdir(child_path):
    #             file_path = child_path.joinpath(file)
    #             file_path.rename(input_path.joinpath(file_path.name))
    #         child_path.rmdir()
    np = NanoporeSequenceData(path=input_path, files_per_dir=3)
    for batch in np:
        print(batch)

