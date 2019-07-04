import yaml
import os

from prefect import Flow, Task

from nanopypes.pipes.basecaller2 import AlbacoreBasecaller
from nanopypes.pipelines import Pipeline
from nanopypes.objects.base import NanoporeSequenceData

class PipelineData:
    data_handlers = {}
    def __init__(self, input_data, data_type):
        self.data_graph = {}

    @property
    def data(self):
        return


def get_config(pipeline, pipes_paths=["../configs/pipes.yml"]):
    all_pipe_configs = {}
    pipeline_configs = {}
    for path in pipes_paths:
        with open(path, 'r') as config:
            all_pipe_configs.update(yaml.safe_load(config))

    for pipe, command in pipeline:
        pipeline_configs[pipe] = all_pipe_configs[pipe]

    return pipeline_configs



class PipelineBuilder(Pipeline):
    pipeline_order = [("albacore", "basecall"), ("minimap2", "map"),
                ("samtools", "sam_to_bam"), ("samtools", "sort_bam"),
                ("samtools", "index_bam"), ("bcftools", "pileup"),
                ("bcftools", "pileup")]

    pipe_handler = {"albacore": AlbacoreBasecaller,
                    "samtools": "Samtools",
                    "minimap2": "Minimap2",
                    "bcftools": "BCFTools"}

    def __init__(self, cluster, pipe_configs, input_path, reference=None, barcode_references=None):
        self.cluster = cluster
        self.num_batches = self.cluster.expected_workers
        self.input = NanoporeSequenceData(path=input_path, num_batches=self.num_batches)
        self.reference = reference
        self.barcode_references = barcode_references
        self.pipeline = Flow(name="variant_caller")
        self.pipe_configs = pipe_configs

        if self.barcode_references and self.reference is None:
            self.demultiplex = True
        else:
            self.demultiplex = False

    def build_pipeline(self):
        bc_save_paths, bc_dependencies = self.add_basecaller(self.input.input_paths)
        if self.demultiplex:
            bc_save_paths, bc_dependencies = self.add_demultiplexer(bc_save_paths, bc_dependencies)
        mapped_save_paths, mapped_dependencies = self.add_mapper(bc_save_paths, bc_dependencies)
        vprep_save_paths, vprep_dependencies = self.add_variant_call_prep(mapped_save_paths, mapped_dependencies)
        variant_save_paths, variant_dependencies = self.add_variant_call(vprep_save_paths, vprep_dependencies)

    def add_basecaller(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["albacore"]
        basecaller = pipe(input_paths=input_paths,
                          save_path=self.save_path,
                          pipe_config=self.pipe_configs["albacore"]["commands"],
                          commands=["basecall"],
                          pipeline=self.pipeline,
                          dependencies=dependencies)

        basecaller.create_tasks()
        return basecaller.expected_data

    def add_demultiplexer(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["demultiplexer"]
        demultiplexer = self.pipe(input_paths=input_paths,
                                  save_path=self.save_path,
                                  command_config=self.pipe_configs["porechop"]["commands"],
                                  commands=["demultiplex"],
                                  pipeline=self.pipeline,
                                  dependencies=dependencies)

        demultiplexer.create_tasks()
        return demultiplexer.expected_data

    def add_mapper(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["minimap2"]
        mapper = pipe(input_paths=input_paths,
                      command_config=self.pipe_configs["minimap2"]["commands"],
                      commands=["splice-map"],
                      pipeline=self.pipeline,
                      dependencies=dependencies)

        mapper.create_tasks()
        return mapper.expected_data

    def add_variant_call_prep(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["samtools"]
        samtools = pipe(input_paths=input_paths,
                        command_config=self.pipe_configs["samtools"]["commands"],
                        commands=["sam_to_bam", "sort_bam", "merge", "index_bam"],
                        pipeline=self.pipeline,
                        dependencies=dependencies)

        samtools.create_tasks()
        return samtools.expected_data

    def add_variant_call(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["bcftools"]
        variant_caller = pipe(input_paths=input_paths,
                              command_config=self.pipe_configs["bcftools"]["commands"],
                              commands=["pileup", "variant_call"],
                              pipeline=self.pipeline,
                              dependencies=dependencies)

        variant_caller.create_tasks()
        return variant_caller.expected_data













if __name__ == '__main__':

    INPUT_DATA = "" # path to data
    DEPENDENCIES = {"albacore": None, "minimap2": ["albacore"], "samtools": ["albacore"], "bcftools": ["samtools"]}
    # Partition input data
    print(CONFIG)



