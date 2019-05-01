import subprocess

from abc import ABC, abstractmethod
import collections.abc


class Pipeline(collections.abc.Callable):
    def __init__(self, pipes):
        self.pipes = pipes

    def __call__(self):
        for pipe in self.pipes:
            pipe()


class Pipe():

    def __init__(self, memory, cpus):
        pass

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


if __name__ == '__main__':
    c = 1048576
    d = 10589934592
    print(d/c)
