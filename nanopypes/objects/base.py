from pathlib import Path
from ont_fast5_api.fast5_file import Fast5File
from ont_fast5_api.multi_fast5 import MultiFast5File


class NanoPypeObject:
    def __init__(self, path):
        self._path = Path(path)

    @property
    def path(self):
        return self._path


class Fast5(Fast5File):
    def __init__(self, path, fast5_type):
        super.__init__(path)


class MultiFast5(MultiFast5File):
    def __init__(self, path, fast5_type):
        super.__init__(path)


class DataSet(NanoPypeObject):
    pass

