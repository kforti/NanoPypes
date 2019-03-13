import os
import subprocess
from pathlib import Path
import re
import shutil

from nanopypes.utils import temp_dirs
from nanopypes.objects.raw import Sample
from nanopypes.config import BasecallConfig


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
                 continue_on=False,
                 last_batch=None):

        self._config = config.basecall
        self.input = Sample(self._config.input_path(input))
        self.flow_cell = self._config.flowcell(flowcell)
        self.kit = self._config.kit(kit)
        self._save_path = Path(self._config.save_path(save_path))
        self.output_format = self._config.output_format(output_format)
        self.reads_per_fastq = self._config.reads_per_fastq(reads_per_fastq)
        self.barcoding = self._config.barcoding(barcoding)
        self.continue_on = continue_on
        if continue_on:
            self.prep_data(last_batch=last_batch)

    @property
    def input_path(self):
        return self.input.path

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
            command = self.build_command(i, str(save_path))
            commands_list.append(command)
        commands_tupl = (next_bin, commands_list)
        return commands_tupl

    @property
    def batches(self):
        batch_pattern = r'(^)[0-9]+($)'
        batches = [Path(self.input_path).joinpath(i) for i in os.listdir(str(self.input_path)) if re.match(batch_pattern, str(i))]
        if self.continue_on:
            for batch in os.listdir(str(self.save_path)):
                if self.input_path.joinpath(batch) in batches:
                    batches.remove(self.input_path.joinpath(batch))
        return batches

    @property
    def num_batches(self):
        return self.input.num_batches

    @property
    def batch_generator(self):
        for bin in self.batches:
            yield bin

    def build_command(self, input_dir, batch_number):
        """ Method for creating the string based command for running the albacore basecaller from the commandline."""
        temp_dir_num = input_dir.split('/')[-1]
        command = ["read_fast5_basecaller.py",]
        command.extend(["--flowcell", self.flow_cell])
        command.extend(["--kit", self.kit])
        command.extend(["--output_format", self.output_format])
        command.extend(["--save_path", str(self._save_path) + "/" + batch_number + "/" + temp_dir_num])
        command.extend(["--worker_threads", "1"])
        command.extend(["--input",  input_dir])
        if self.barcoding:
            command.append("--barcoding")
        if self.output_format == "fastq":
            command.extend(["--reads_per_fastq", str(self.reads_per_fastq)])
        return command

    @classmethod
    def build_func(self):
        def func(command):
            process = subprocess.check_output(command)
            return process
        return func

    def prep_data(self, last_batch=None):
        if not last_batch:
            last_batch = self._find_last_batch()
        if last_batch:
            print("LAST BATCH: ", last_batch, "Deleting the last batch......")
            shutil.rmtree(str(last_batch))
        if self.input_path.joinpath('split_data').exists():
            print("DELETING SPLIT DATA...")
            shutil.rmtree(str(self.input_path.joinpath('split_data')))

    def _find_last_batch(self):
        for batch in os.listdir(str(self.save_path)):
            split = os.listdir(str(self.save_path.joinpath(batch)))[0]
            files = [file for file in os.listdir(str(self.save_path.joinpath(batch, split)))]
            if 'sequencing_telemetry.js' not in files:
                return self.save_path.joinpath(batch)
            else:
                continue



