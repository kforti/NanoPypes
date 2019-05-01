import os
from pathlib import Path
import subprocess
import logging

from nanopypes.pipes.base import Pipe



class MiniMap2(Pipe):
    commands = {'genomic': 'minimap2 -ax map-ont %(ref)s %(read)s > %(output)s',
                'splice': 'minimap2 -ax splice %(ref)s %(read)s > %(output)s',
                'rna': 'minimap2 -ax splice -uf -k14 %(ref)s %(read)s > %(output)s',
                'overlap': 'minimap2 -x ava-ont %(ref)s %(read)s > %(output)s'}

    def __init__(self, input_path, reference, client, save_path, command):
        self.client = client
        self.reference = Path(reference)
        self.save_path = Path(save_path)
        self.input = Path(input_path)

        if command not in self.commands.keys():
            raise KeyError("Command not available. Please select one of the following\n{}".format(self.commands.keys()))
        self.command = self.commands[command]

        if self.input.is_dir():
            self.input_type = 'dir'
        elif self.input.is_file():
            self.input_type = 'file'

        self.all_alignments = []

    def execute(self):
        if self.input_type == 'dir':
            for fastq in os.listdir(str(self.input)):
                fastq = self.input.joinpath(fastq)
                mmap = self.create_subprocess(fastq)
                alignments = self.client.submit(mmap)
                self.all_alignments.append(alignments)
            self.client.gather(self.all_alignments)
        return

    def create_subprocess(self, fastq):
        fastq_extension = "".join(fastq.suffixes)
        #print(fastq_extension)
        samfile = self.save_path.joinpath(str(fastq).replace(fastq_extension, '.sam'))

        command_args = {'ref': str(self.reference),
                        'read': str(fastq),
                        'output': str(samfile)}

        #print(command_args)
        command = self.command % command_args
        command = command.split()
        #print(command)

        def subp():
            logging.info(("Running command %s" % command), level=logging.DEBUG)
            result = subprocess.run(command, shell=True)
            return
        return subp
