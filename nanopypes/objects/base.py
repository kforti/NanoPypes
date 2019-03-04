from pathlib import Path
from ont_fast5_api.fast5_file import Fast5File


class NanoPypeObject:
    def __init__(self, path):
        self._path = Path(path)
        self.check_data()

    @property
    def path(self):
        return self._path

    def check_data(self):
        return 0


class Fast5(Fast5File):
    pass
