import subprocess
import logging
from pathlib import Path
from abc import ABC, abstractmethod
import collections.abc

from nanopypes.utils import temp_dirs, remove_temps, collapse_save, ParallelizeData


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


class AlbacoreBasecall(Pipe):
    def __init__(self, albacore, compute):
        self.compute = compute
        self.albacore = albacore
        self.func = self.albacore.build_func()
        self.input_path = Path(self.albacore.input_path)
        self.temp_path = self.input_path.joinpath("temp")

        self.compute.connect()

    def execute(self):
        batch_counter = 0
        batches = len(self.albacore.batches)
        for batch in self.albacore.batches:
            batch_counter += 1
            pdata = ParallelizeData()
            pdata.split_data(self.input_path)
            dirs = temp_dirs(batch, self.input_path)
            commands = []
            for dir in dirs:
                commands.append(self.albacore.build_command(dir, batch.name))
            self.compute.map(self.func, commands)
            print("\nBatch ", batch_counter, " out of ", batches)
            self.compute.show_progress()

            remove_temps(self.temp_path)
        basecalled_data = collapse_save(self.albacore.save_path)
        return basecalled_data

