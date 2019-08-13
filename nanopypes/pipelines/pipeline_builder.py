from prefect import Flow

from nanopypes.distributed_data.pipeline_data import BuildCommands
from nanopypes.distributed_data.partition_data import DataPartitioner, get_structure
from nanopypes.pipes.base2 import Pipe

import math
import os

def determine_partition_strategy(directory, partitions=None, batch_size=None):

    structure, children = get_structure(directory)
    if batch_size is None and partitions:
        batch_size = math.ceil(len(children) / partitions)
    elif partitions is None and batch_size:
        partitions = math.ceil(len(children) / batch_size)
    #print("children: ", len(children))
    #print(partitions)
    #print(batch_size)
    return batch_size, partitions


class PipelineBuilder:

    def __init__(self, inputs, pipeline_order, pipeline_name, pipe_specs, partitions=None, batch_size=None):
        self.pipe_specs = pipe_specs
        self.num_batches = len(inputs)
        self.pipeline_order = pipeline_order
        self.pipeline_order_gen = iter(self.pipeline_order)
        self.inputs = inputs
        self.num_partitions = partitions
        self.batch_size = batch_size

        self._pipeline = Flow(name=pipeline_name)

        self.transformation_matrices = {}
        self.data_partition_matrices = {}
        self.num_matrices = 0

    @property
    def pipeline(self):
        return self._pipeline

    def build_tasks(self):
        self.tool = None
        self.prev_tool = None
        self.command = None
        self.prev_command = None

        tools_cmds, batch_sizes, all_partitions = self._get_matrix_info()
        for i in range(len(tools_cmds)):
            self._build_matrices(tools_cmds[i], all_partitions[i], matrix_num=i)

        return

    def _get_matrix_info(self):
        batch_size, partitions = determine_partition_strategy(directory=self.inputs[0][0], partitions=self.num_partitions,
                                                              batch_size=self.batch_size)
        #print("partitions", partitions)

        all_tools_cmd = []
        tool_cmd = []
        batch_sizes = [batch_size]
        all_partitions = [partitions]
        for tool, command in self.pipeline_order:
            if self.pipe_specs[tool]["commands"][command]["merge"] == True:
                all_tools_cmd.append(tool_cmd)
                tool_cmd = [(tool, command)]
                batch_sizes.append(self.pipe_specs[tool]["commands"][command]["batch_size"])
                all_partitions.append(self.pipe_specs[tool]["commands"][command]["partitions"])
            else:
                tool_cmd.append((tool, command))
        all_tools_cmd.append(tool_cmd)
        #print("all_partitions: ", all_partitions)
        return all_tools_cmd, batch_sizes, all_partitions

    def _build_matrices(self, transforms, partitions, matrix_num):
        transformation_matrix = []
        partition_matrix = []
        # print("t : ", transforms)
        # print("p : ", partitions)
        for tool, command in transforms:
            self._load_transform(tool, command)
            transform_task_id = "_".join([tool, command])
            # if self.partition is True:
            #     partition_result = self._partition_data()

            pipe = Pipe(task_id=transform_task_id,
                        template=self.command_template,
                        task_type=self.task_type,
                        **self.task_kwargs
                        )
            pipe_tasks = pipe.create_tasks(partitions)
            transformation_matrix.append(pipe_tasks)

            partition_task_id = 'data_partition_{}'.format(transform_task_id)
            data_partitioner = DataPartitioner(num_batches=partitions,
                                               save_path=self.save_path,
                                               # batch_size=self.batch_size,
                                               partitions=partitions,
                                               prev_tool=self.prev_tool,
                                               prev_cmd=self.prev_command,
                                               next_tool=self.tool,
                                               next_cmd=self.command,
                                               name=partition_task_id,
                                               slug=partition_task_id,
                                               )
            partition_tasks = data_partitioner.partition_data()
            partition_matrix.append(partition_tasks)

        self.num_matrices += 1
        self.transformation_matrices[matrix_num] = transformation_matrix
        self.data_partition_matrices[matrix_num] = partition_matrix
        # print("transform_matrices", self.transformation_matrices)
        # print("partition matrices", self.data_partition_matrices)

    def _partition_data(self, inputs, tasks):
        task = tasks[0]
        batches = inputs[0]

        with self._pipeline as flow:
            partition_result = task(batches=batches)

        return partition_result

    def _merge_data(self, inputs, tasks, dependencies):
        task = tasks[0]
        batches = inputs

        with self._pipeline as flow:
            partition_result = task(batches=batches, dependencies=dependencies)
            #partition_result.set_dependencies(dependencies)

        return partition_result

    def _add_merge_pipes(self, partition_result, tasks):
        pipe_results = {}

        for i, task in enumerate(tasks):
            with self._pipeline as flow:
                pipe_result = task(command_data=partition_result, batch_num=i, is_initial=False)
            pipe_results[i] = pipe_result

        return pipe_results

    def _add_paritioned_pipes(self, partition_result, tasks):
        pipe_results = {}

        for i, task in enumerate(tasks):
            with self._pipeline as flow:
                pipe_result = task(command_data=partition_result, batch_num=i, is_initial=True)
            pipe_results[i] = pipe_result

        return pipe_results


    def build_pipeline(self):
        #matrix_inputs = self.inputs
        # partition_batches = len(self.inputs)
        # partition_batch_counter = 0
        partition = True
        merge = False
        prev_pipe_result = None
        for i in range(self.num_matrices):
            partition_matrix = self.data_partition_matrices[i]
            pipe_matrix = self.transformation_matrices[i]
            if partition is True:
                partition_results = self._partition_data(inputs=self.inputs, tasks=partition_matrix[0])
                pipe_results = self._add_paritioned_pipes(partition_result=partition_results, tasks=pipe_matrix[0])
                partition = False
                merge = True
            elif merge:
                partition_results = self._merge_data(inputs=self.inputs, tasks=partition_matrix[0], dependencies=matrix_results)
                pipe_results = self._add_merge_pipes(partition_result=partition_results, tasks=pipe_matrix[0])
                continue

            num_transforms = len(pipe_matrix)
            num_partitions = len(pipe_matrix[0])
            matrix_results = []
            matrix_inputs = []

            for partition_index in range(1, num_partitions):
                inputs = partition_results

                for transform_index in range(1, num_transforms):
                    #print("ti: ", transform_index)
                    #print("pi", partition_index)
                    if transform_index == 1:
                        pipe_result = pipe_results[partition_index]
                        partition_num = partition_index
                    else:
                        partition_num = None


                    pass_data_result = self._add_pass_data_tasks(
                            task=partition_matrix[transform_index][partition_index], inputs=inputs, batch_num=partition_index,
                            pipe_results=pipe_result, partition_num=partition_num)
                    inputs = pass_data_result
                    pipe_result = self._add_pipe_tasks(data_result=inputs, batch_num=None, task=pipe_matrix[transform_index][partition_index], prev_pipe_result=prev_pipe_result)


                    if transform_index == num_transforms - 1:
                        print("adding")
                        matrix_results.append(pipe_result)
                        matrix_inputs.append(pass_data_result)
            self.inputs = matrix_inputs

    def _add_pass_data_tasks(self, task, inputs, batch_num=None, pipe_results=None, partition_num=None):
        with self._pipeline as flow:
            partition_result = task(batches=inputs, batch_num=batch_num, dependencies=pipe_results, partition_num=partition_num)

        return partition_result

    def _add_pipe_tasks(self, task, data_result, prev_pipe_result, is_initial=False, batch_num=None):
        with self._pipeline as flow:
            pipe_result = task(command_data=data_result, batch_num=batch_num, is_initial=is_initial)
            if prev_pipe_result:
                pipe_result.set_upstream(prev_pipe_result)

        return pipe_result

    def _load_transform(self, tool, command):
        if tool not in self.pipe_specs or command not in self.pipe_specs[tool]["commands"]:
            raise Exception("The tool and command you entered does not match the pipe_spec")
        if self.tool:
            self.prev_tool = self.tool
        if self.command:
            self.prev_command = self.command

        #self.partition = self.pipe_specs[tool]['commands'][command]['partitions']
        self.tool = tool
        self.command = command
        self.save_path = self.pipe_specs[tool]["save_path"]
        try:
            self.batch_size = self.pipe_specs[tool]['commands'][command]['batch_size']
        except:
            pass
        try:
            self.partitions = self.pipe_specs[tool]['commands'][command]['partitions']
        except:
            pass
        self.command_template = self.pipe_specs[tool]['commands'][command]['template']
        self.task_type = self.pipe_specs[self.tool]['task_type']
        #self.merge = self.pipe_specs[tool]['commands'][command]['merge']
        self.task_kwargs = self.pipe_specs[self.tool]['task_kwargs']
        # self.pipe_tasks = []
        # self.partition_tasks = []
        # self.save_batches = []

        return

if __name__ == '__main__':
    from nanopypes.utilities import PipelineConfiguration
    from distributed import LocalCluster
    from prefect.engine.executors.dask import DaskExecutor

    cluster = LocalCluster()
    executor = DaskExecutor(cluster.scheduler_address)

    path = "../configs/pipelines/pipeline.yml"
    user_input = {'flowcell': 'FLO-MIN106',
                  'kit': 'SQK-LSK109',
                  'reference': '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/lambda_reference.fasta'}
    config = PipelineConfiguration(path, user_input)

    inputs = [["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"]]
    pipe_specs = config.pipe_configs
    print(pipe_specs)
    pb = PipelineBuilder(inputs=inputs,
                         pipeline_order=config.pipeline_order,
                         pipeline_name="test-pipeline",
                         pipe_specs=pipe_specs,
                          batch_size=2)
    pb.build_tasks()
    #print('provenance', pb.data_provenance)
    pb.build_pipeline()
    pb.pipeline.visualize()
    pb.pipeline.run(executor=executor)
