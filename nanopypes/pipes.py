import subprocess
import os
import re
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
import collections.abc

from nanopypes.utils import remove_splits, collapse_save, split_data
from nanopypes.compute import Cluster
from nanopypes.objects.base import DataSet


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
    def __init__(self, albacore, compute, data_splits, parallel_batches=10):
        print("Configuring albacore pipe.... ")
        self.compute = compute
        self.albacore = albacore
        self.func = self.albacore.build_func()
        self.input_path = Path(self.albacore.input_path)
        self.save_path = Path(self.albacore.save_path)
        self.splits_paths = []
        self.parallel_batches = parallel_batches
        self.batch_splits = data_splits

    def execute(self):
        batch_counter = 0
        batches = len(self.albacore.batches)
        commands = []
        maps = 1
        for batch in self.albacore.batches:
            batch_counter += 1
            self.splits_paths.append(self.input_path.joinpath(batch.name, 'split_data'))
            split_data(data_path=batch,
                       save_path=self.input_path.joinpath(batch.name),
                       splits=self.batch_splits,
                       compute=self.compute)

            for split in range(self.batch_splits):
                commands.append(self.albacore.build_command(str(self.input_path.joinpath(batch.name, 'split_data', str(split))), batch.name))
            if batch_counter == self.parallel_batches:
                print("\nBatches ", (batch_counter * maps - self.parallel_batches), " - ", (batch_counter * maps), " out of ", batches)
                try:
                    self.compute.map(self.func, commands)
                except Exception as e:
                    print(e)
                #self.compute.show_progress()
                
                self.compute.map(remove_splits, self.splits_paths)
                maps += 1
                batch_counter = 0
                commands = []
                self.splits_paths = []

        basecalled_data = collapse_save(self.albacore.save_path)
        return #basecalled_data

    def remove_parallel_data(self, path=None):
        if path == None:
            path = self.save_path
        batch_pattern = r'(^)[0-9]+($)'
        for batch in os.listdir(str(self.save_path)):
            if re.match(batch_pattern, batch):
                shutil.rmtree(str(self.save_path.joinpath(batch)))
            else:
                continue


class RsyncParallel(Pipe):

    def __init__(self, data_path, local, remote, *options):
        """Can handle moving raw data on the sequence output, experiment and sample levels, where sequence output consists of multiple experiments,
         experiments consist of multiple samples and sample consists of the results from one sequencing run."""
        self.data_set = DataSet(data_path)
        self.options = options
        self.local = local
        self.remote = remote
        self.compute = Cluster(cluster_type='local')

    def execute(self):
        data_type = self.data_set.data_type


########################################################
###### MiniMap2 Pipe
########################################################

class MiniMap2(Pipe):
    def __init__(self, fastq_path, reference, compute, save_path):
        self.compute = compute
        self.fastq_path = Path(fastq_path)
        self.fastq_paths = [str(self.fastq_path.joinpath(file)) for file in os.listdir(str(self.fastq_path))]
        self.reference = Path(reference)
        self.save_path = Path(save_path)

    @property
    def info(self):
        print("Fastq Paths: \n", self.fastq_paths)

    def execute(self):
        func = minimap_func(self.save_path, self.reference)
        self.compute.map(func, self.fastq_paths)
        close = False
        while close != True:
            close = bool(input("Close? "))
        self.compute.close()


def minimap_func(save_path, reference):
    def mapper(fastq_path):
        fastq = Path(fastq_path)
        sam_file = save_path.joinpath((fastq.name.replace('.fq', '.sam')))
        command = ['/Users/kevinfortier/minimap2/minimap2/minimap2', '-ax', 'map-ont', str(reference), str(fastq), '>', str(sam_file).replace('.gz', '')]
        #command = '/Users/kevinfortier/minimap2/minimap2/minimap2 -ax map-ont ' + str(reference) + ' ' + str(fastq) + ' > ' + str(sam_file).replace('.gz', '')
        print(command)
        process = subprocess.check_output(command)
        return process
    return mapper


########################################################
###### SamToBam Pipe
########################################################

class SamToBam(Pipe):
    def __init__(self, sam, bam, compute):
        self.sam = Path(sam)
        self.bam = Path(bam)
        self.compute = compute

    def execute(self):
        func = sam_to_bam_func(self.sam, self.bam)
        self.compute.map(func, )



def sam_to_bam_func(sam, bam):
    def sam_to_bam(sam):
        pass
    return sam_to_bam

########################################################
###### SortBam Pipe
########################################################

class SortBam(Pipe):
    def __init__(self, bam, save_path):
        pass


def sort_bam_func():
    def sort_bam():
        pass
    return sort_bam

########################################################
###### PileUp Pipe
########################################################

class PileUp(Pipe):
    def __init__(self, reference, sorted_bam, save_path):
        pass


def pileup_func():
    def pileup():
        pass
    return pileup

########################################################
###### VariantCall Pipe
########################################################

class VariantCall(Pipe):
    def __init__(self, bcf, vcf):
        pass


def variant_call_func():
    def variant_call():
        pass
    return variant_call


if __name__ == '__main__':
    print([cls.__name__ for cls in Pipe.__subclasses__()])
