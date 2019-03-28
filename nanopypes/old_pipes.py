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
from nanopypes.objects.basecalled import ParallelBaseCalledData


class Pipeline(collections.abc.Callable):
    def __init__(self, pipes):
        self.pipes = pipes

    def __call__(self):
        for pipe in self.pipes:
            pipe()






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
