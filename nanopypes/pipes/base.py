import subprocess

from abc import ABC, abstractmethod
import collections.abc


class Pipeline(collections.abc.Callable):
    def __init__(self, pipes):
        self.pipes = pipes

    def __call__(self):
        for pipe in self.pipes:
            pipe()


class Pipe(ABC):

    _requirements = "No requirements have been added to this Pipe"

    @abstractmethod
    def execute(self):
        pass

    def install(self):
        #TODO check that conda is installed
        raise NotImplementedError

    @property
    def requirements(self):
        print(self._requirements)

    def install_conda(self):
        raise NotImplementedError

    @classmethod
    def use_bioconda(cls):
        raise NotImplementedError

    def __call__(self):
        return self.execute()
