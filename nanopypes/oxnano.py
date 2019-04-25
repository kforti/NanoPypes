import os
import subprocess
from pathlib import Path
import re
import shutil

from nanopypes.objects.raw import Sample

class Albacore:
    """ Conatains the data associated with making the command to run the basecaller.
    Build the command with build_command()
   """
    def __init__(self, config=None,
                 input_path=None,
                 flowcell=None,
                 kit=None,
                 save_path=None,
                 output_format=None,
                 reads_per_fastq=1000):

        #self._config = config.basecall
        self.input = Sample(input_path)#self._config.input_path(input_path))
        self.flow_cell = flowcell#self._config.flowcell(flowcell)
        self.kit = kit#self._config.kit(kit)
        self._save_path = Path(save_path)#self._config.save_path(save_path))
        if self._save_path.exists() == False:
            self._save_path.mkdir()
        self._output_format = output_format#self._config.output_format(output_format)
        self.reads_per_fastq = reads_per_fastq#self._config.reads_per_fastq(reads_per_fastq)
        self._bc_batches = os.listdir(str(self._save_path))

    @property
    def bc_batches(self):
        return self._bc_batches

    @bc_batches.setter
    def bc_batches(self, batches):
        self._bc_batches = batches

    @property
    def input_path(self):
        return self.input.path

    @property
    def output_format(self):
        return self._output_format

    @property
    def save_path(self):
        return self._save_path

    # @property
    # def config(self):
    #     return self._config
    #
    # @config.setter
    # def config(self, conf):
    #     self._config = conf

    def all_batches(self):
        batch_pattern = r'(^)[0-9]+($)'
        batches = [Path(self.input_path).joinpath(i) for i in os.listdir(str(self.input_path)) if re.match(batch_pattern, str(i))]
        return batches

    @property
    def batches_for_basecalling(self):
        batch_pattern = r'(^)[0-9]+($)'
        batches = [Path(self.input_path).joinpath(i) for i in os.listdir(str(self.input_path)) if re.match(batch_pattern, str(i)) and i not in self._bc_batches]

        return batches

    @property
    def num_batches(self):
        return self.input.num_batches

    @property
    def batch_generator(self):
        for bin in self.batches_for_basecalling:
            yield bin

    def build_basecall_command(self, input_dir):
        """ Method for creating the string based command for running the albacore basecaller from the commandline."""
        command = ["read_fast5_basecaller.py",]
        command.extend(["--flowcell", self.flow_cell])
        command.extend(["--kit", self.kit])
        command.extend(["--output_format", self._output_format])
        command.extend(["--save_path", str(self._save_path.joinpath(input_dir.name))])
        command.extend(["--worker_threads", "1"])
        command.extend(["--input",  str(input_dir)])

        if self._output_format == "fastq":
            command.extend(["--reads_per_fastq", str(self.reads_per_fastq)])
        return command

    @classmethod
    def build_func(self):
        def func(command):
            process = subprocess.run(command, check=True)
            return
        return func

