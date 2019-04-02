import os
from pathlib import Path
import subprocess

from nanopypes.pipes.base import Pipe




class MiniMap2(Pipe):
    commands = {'genomic': 'minimap2 -ax map-ont ref.fa ont.fq.gz > aln.sam',
                'splice': 'minimap2 -ax splice ref.fa rna-reads.fa > aln.sam',
                'rna': 'minimap2 -ax splice -uf -k14 ref.fa reads.fa > aln.sam',
                'overlap': 'minimap2 -x ava-ont reads.fa reads.fa > overlaps.paf'}

    def __init__(self, input_path, reference, client, save_path, command):
        self.client = client
        self.reference = Path(reference)
        self.save_path = Path(save_path)
        self.input = Path(input_path)

        if command not in self.commands.keys():
            raise KeyError("Command not available. Please select one of the follow\n{}".format(self.commands.keys()))
        self.command = command

        if self.input.is_dir():
            self.input_type = 'dir'
        elif self.input.is_file():
            self.input_type = 'file'

        self.all_alignments = []

    def execute(self):
        if self.input_type == 'dir':
            for fastq in os.listdir(str(self.input)):
                mmap = self.create_subprocess(fastq)
                alignments = self.client.submit(mmap)
                self.all_alignments.append(alignments)
            self.client.gather(self.all_alignments)


    def create_subprocess(self, fastq):
        samfile = self.save_path.joinpath(fastq.replace('fq', 'sam'))
        if self.command == 'splice':
            command = ['minimap2', '-ax', 'splice', str(self.reference), str(self.input.joinpath(fastq)), '>', str(self.save_path)]
            print(command)
        def subp():
            result = subprocess.check_output(command)
            return result
        return subp



if __name__ == '__main__':
    minimapper = MiniMap2()
