import yaml
import os

from prefect import Flow, Task
from prefect.engine.executors.dask import DaskExecutor

from nanopypes.pipes.basecaller2 import AlbacoreBasecaller
from nanopypes.pipes.long_read_mappers import MiniMap2
from nanopypes.pipes.demultiplex import Porechop
from nanopypes.distributed_data.base import NanoporeSequenceData
from nanopypes.tasks.base import GetFastqs

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


class PipelineBuilder:
    # pipeline_order = [("albacore", "basecall"), ("porechop", "demultiplex"), ("minimap2", "map"),
    #             ("samtools", "sam_to_bam"), ("samtools", "sort_bam"),
    #             ("samtools", "index_bam"), ("bcftools", "pileup"),
    #             ("bcftools", "pileup")]

    pipe_handler = {"albacore": AlbacoreBasecaller,
                    "samtools": "Samtools",
                    "minimap2": MiniMap2,
                    "bcftools": "BCFTools",
                    "demultiplex": Porechop}

    def __init__(self, cluster_manager, pipeline_order, input_path, save_path, pipe_configs):
        self.cluster_manager = cluster_manager
        self.executor = DaskExecutor(self.cluster_manager.cluster)
        self.save_path = save_path
        self.num_batches = 1#int(self.cluster.expected_workers / 2)
        self.input = NanoporeSequenceData(path=input_path, batch_size=self.num_batches)
        self._pipeline = Flow(name="variant_caller")
        self.pipe_configs = pipe_configs
        self.pipeline_order = pipeline_order

        # if self.barcode_references and self.reference is None:
        #     self.demultiplex = True
        # else:
        self.demultiplex = ('porechop' in self.pipeline_order)

        self._all_commands = {}

    @property
    def all_commands(self):
        return self._all_commands

    @property
    def pipeline(self):
        return self._pipeline

    def run(self):
        self.pipeline.run(executor=self.executor)

    def build_pipeline(self):
        bc_save_paths, bc_dependencies = self.add_basecaller([i for i in self.input])
        if self.demultiplex:
            bc_save_paths, bc_dependencies = self.add_demultiplexer(bc_save_paths, bc_dependencies)
        elif self.demultiplex is False:
            fastq_save_paths = []
            for i, path in enumerate(bc_save_paths):
                task = GetFastqs(path)
                if bc_dependencies:
                    task.set_upstream(bc_dependencies[i], flow=self._pipeline)
                else:
                    self._pipeline.add_task(task)
                fastq_save_paths.append(task)
            bc_save_paths = fastq_save_paths



        mapped_save_paths, mapped_dependencies = self.add_mapper(bc_save_paths, bc_dependencies)
        #vprep_save_paths, vprep_dependencies = self.add_variant_call_prep(mapped_save_paths, mapped_dependencies)
        #variant_save_paths, variant_dependencies = self.add_variant_call(vprep_save_paths, vprep_dependencies)

    def add_basecaller(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["albacore"]
        basecaller = pipe(input_paths=input_paths,
                          save_path=self.save_path,
                          command_config=self.pipe_configs["albacore"]["commands"],
                          commands=["basecall"],
                          pipeline=self._pipeline,
                          dependencies=dependencies,
                          task_config=self.pipe_configs["albacore"]["task_config"])
        self._pipeline.update(basecaller.create_tasks())
        self._all_commands.update(basecaller.all_commands)
        return basecaller.expected_data

    def add_demultiplexer(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["demultiplex"]
        demultiplexer = pipe(input_paths=input_paths,
                                  save_path=self.save_path,
                                  command_config=self.pipe_configs["porechop"]["commands"],
                                  commands=["demultiplex"],
                                  pipeline=self._pipeline,
                                  dependencies=dependencies,
                                  task_config=self.pipe_configs["porechop"]["task_config"])

        self._pipeline.update(demultiplexer.create_tasks())
        self._all_commands.update(demultiplexer.all_commands)
        return demultiplexer.expected_data

    def add_mapper(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["minimap2"]
        mapper = pipe(input_paths=input_paths,
                      save_path=self.pipe_configs["minimap2"]["save_path"],
                      reference=self.pipe_configs["minimap2"]["references"],
                      command_config=self.pipe_configs["minimap2"]["commands"],
                      commands=["splice-map"],
                      pipeline=self._pipeline,
                      dependencies=dependencies,
                      task_config=self.pipe_configs["minimap2"]["task_config"])

        self._pipeline.update(mapper.create_tasks())
        self._all_commands.update(mapper.all_commands)
        return mapper.expected_data

    def add_variant_call_prep(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["samtools"]
        samtools = pipe(input_paths=input_paths,
                        command_config=self.pipe_configs["samtools"]["commands"],
                        commands=["sam_to_bam", "sort_bam", "merge", "index_bam"],
                        pipeline=self.pipeline,
                        dependencies=dependencies,
                        task_config=self.pipe_configs["samtools"]["task_config"])

        samtools.create_tasks()
        return samtools.expected_data

    def add_variant_call(self, input_paths, dependencies=None):
        pipe = self.pipe_handler["bcftools"]
        variant_caller = pipe(input_paths=input_paths,
                              command_config=self.pipe_configs["bcftools"]["commands"],
                              commands=["pileup", "variant_call"],
                              pipeline=self.pipeline,
                              dependencies=dependencies,
                              task_config=self.pipe_configs["bcftools"]["task_config"])

        variant_caller.create_tasks()
        return variant_caller.expected_data











if __name__ == '__main__':
    from distributed import LocalCluster
    from nanopypes import ClusterManager

    cluster = ClusterManager(cluster=LocalCluster())
    input_path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/"
    save_path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy"

    pb = PipelineBuilder(cluster_manager=cluster, input_path=input_path, save_path=save_path)
    pb.build_pipeline()
    print(pb.pipeline.__dict__)



