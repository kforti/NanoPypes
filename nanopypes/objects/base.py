from pathlib import Path
from ont_fast5_api.fast5_file import Fast5File


class NanoPypeObject:
    def __init__(self, path):
        self._path = Path(path)

    @property
    def path(self):
        return self._path


class Fast5(Fast5File):
    pass

class DataSet(NanoPypeObject):
    pass

