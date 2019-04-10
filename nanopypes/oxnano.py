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
    def __init__(self, config,
                 input=None,
                 flowcell=None,
                 kit=None,
                 save_path=None,
                 output_format=None,
                 reads_per_fastq=None,
                 barcoding=None,
                 continue_on=False):

        self._config = config.basecall
        self.input = Sample(self._config.input_path(input))
        self.flow_cell = self._config.flowcell(flowcell)
        self.kit = self._config.kit(kit)
        self._save_path = Path(self._config.save_path(save_path))
        self._output_format = self._config.output_format(output_format)
        self.reads_per_fastq = self._config.reads_per_fastq(reads_per_fastq)
        self._barcoding = self._config.barcoding(barcoding)
        self.continue_on = continue_on
        self._bc_batches = []

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
    def barcoding(self):
        return self._barcoding

    @property
    def save_path(self):
        return self._save_path

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, conf):
        self._config = conf

    @property
    def basecall_input(self):
        """ Retrive the name of the input directory and the list of commands
         associated with that directory as a dict {dir_name: [List of commands}"""
        next_bin = next(self.batch_generator)
        bin_path = Path(self.input_path).joinpath(next_bin)
        tmp_dirs = temp_dirs(bin_path, self.input.path)
        commands_list = []

        # Make sure the save-path is created
        save_path = self._save_path.joinpath(next_bin)
        if not save_path.exists():
            save_path.mkdir()

        for i in tmp_dirs:
            command = self.build_basecall_command(i, str(save_path))
            commands_list.append(command)
        commands_tupl = (next_bin, commands_list)
        return commands_tupl

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

    def build_basecall_command(self, input_dir, batch_number, save_path=None):
        """ Method for creating the string based command for running the albacore basecaller from the commandline."""
        temp_dir_num = input_dir.split('/')[-1]
        command = ["read_fast5_basecaller.py",]
        command.extend(["--flowcell", self.flow_cell])
        command.extend(["--kit", self.kit])
        command.extend(["--output_format", self._output_format])
        if save_path:
            command.extend(["--save_path", str(save_path)])
        else:
            command.extend(["--save_path", str(self._save_path) + "/" + batch_number + "/" + temp_dir_num])
        command.extend(["--worker_threads", "1"])
        command.extend(["--input",  input_dir])
        if self._barcoding:
            command.append("--barcoding")
        if self._output_format == "fastq":
            command.extend(["--reads_per_fastq", str(self.reads_per_fastq)])
        return command

    @classmethod
    def build_func(self):
        def func(command):
            process = subprocess.check_output(command)
            return process
        return func

    def prep_data(self):
        ## delete directories that have been half
        for batch in os.listdir(str(self.input_path)):
            if 'split_data' in os.listdir(str(self.input_path.joinpath(batch))):
                splits = os.listdir(str(self.input_path.joinpath('split_data')))
                if splits == 0:
                    continue

                try:
                    print("DELETING SPLIT DATA...")
                    shutil.rmtree(str(self.input_path.joinpath(batch, 'split_data')))
                except FileNotFoundError:
                    pass
                try:

                    print("LAST BATCH: ", batch, "Deleting the last basecalled batch......")

                    shutil.rmtree(str(self.save_path.joinpath(batch)))
                except Exception as e:
                    pass


if __name__ == "__main__":
   pass

