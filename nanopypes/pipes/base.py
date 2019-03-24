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

    def build_func(self, func_type, func=None):
        def subp(command):
            process = subprocess.check_output(command)
            return process

        if func_type == "subprocess":
            return subp

        elif func_type == "custom":
            if func == None:
                raise ValueError("You must include a function with this method")
            return func

    @abstractmethod
    def execute(self):
        pass

    def __call__(self):
        return self.execute()
