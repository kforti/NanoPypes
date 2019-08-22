from prefect import Flow

from nanopypes.distributed_data.partition_data import *
from nanopypes.core.data_transform import DataTransform
from nanopypes.tasks.partition_file_data import PartitionFileData, MergeFileData

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

    def __init__(self, inputs, save_path, pipeline_order, pipeline_name, pipe_specs, partitions=None, batch_size=None):
        self._pipeline = Flow(name=pipeline_name)
        self.pipe_specs = pipe_specs
        self.pipeline_order = pipeline_order
        self.save_path = save_path

        # Task attributes

        self.next_tool_cmd = None

        # Matrix attributes
        self.inputs = inputs
        self.num_partitions = partitions
        self.batch_size = batch_size
        self.transformation_matrices = {}
        self.data_partition_matrices = {}
        self.num_matrices = 0
        self.prev_transform_id = None

        self.partition_strategy_handler = {"ont_sequence": ont_partition_strategy}

        self.kwargs_handler = {
            "albacore_basecall":
                {
                    "no_prev": {'partitions': self.num_partitions, 'batch_size': self.batch_size,
                                'save_path': self.save_path},
                    "partition": {},
                    "merge": {}
                },
            "minimap2_splice-map":
                {
                    "no_prev": {},
                    "albacore_basecall": {'save_path': self.save_path, 'next_tool_cmd': self.next_tool_cmd},
                    # 'strategy': self.split_merge, 'input_type': 'fastq'},
                    "porechop_demultiplex": {'save_path': self.save_path},
                },
            "porechop_demultiplex":
                {
                    "no_prev": {},
                    "albacore_basecall": {'save_path': self.save_path, 'next_tool_cmd': self.next_tool_cmd}
                    # 'strategy': self.split_merge, 'input_type': 'main_dir'}
                },
            "samtools_sam_to_bam":
                {
                    "no_prev": {},
                    "minimap2_splice-map": {}
                },
            "samtools_merge_bams":
                {
                    "no_prev": {},
                    "samtools_sam_to_bam": {'save_path': self.save_path}
                },

        }

        self.func_handler = {
            "albacore_basecall":
                {
                    "no_prev": extract_partitioned_directories(),
                    "partition": partition_ont_seq_data,
                    "merge": {}
                },
            "minimap2_splice-map":
                {
                    "no_prev": {},
                    "albacore_basecall": partition_basecalled_data,
                    "porechop_demultiplex": partition_demultiplexed_data,
                },
            "porechop_demultiplex":
                {
                    "no_prev": {},
                    "albacore_basecall": partition_basecalled_data
                },
            "samtools_sam_to_bam":
                {
                    "no_prev": {},
                    "minimap2_splice-map": sam_to_bam
                },
            "samtools_merge_bams":
                {
                    "no_prev": {},
                    "samtools_sam_to_bam": merge_bams
                },
        }

    @property
    def pipeline(self):
        return self._pipeline

    def build_tasks(self):
        self.tool = None
        self.prev_tool = None
        self.command = None
        self.prev_command = None

        # tools_cmds, batch_sizes, all_partitions = self._get_matrix_info()
        # for i in range(len(tools_cmds)):
        #     self._build_matrices(tools_cmds[i], all_partitions[i], matrix_num=i)

        for i, matrix_id in enumerate(self.pipeline_order):
            is_initial = True
            matrix = self.pipeline_order[matrix_id]
            self.pipeline_order[matrix_id]["transform_tasks"] = []

            matrix = self.build_transform_matrix(matrix, is_initial)
            matrix = self._build_merge_transforms(matrix)
            matrix["num_batches"] = self.num_batches

        return

    def _build_merge_transforms(self, matrix):
        merge_transforms = matrix["merge_transforms"]
        for index, merge_tool_cmd in merge_transforms.items():
            from_tool, from_cmd = matrix["data_transform_order"][index]
            merge_task = self._create_merge_task(from_tool, from_cmd, merge_tool=merge_tool_cmd[0],
                                                 merge_cmd=merge_tool_cmd[1])
            if "merge_tasks" not in matrix:
                matrix["merge_tasks"] = {}
            transform_id = "{}_{}".format(merge_tool_cmd[0], merge_tool_cmd[1])
            matrix["merge_tasks"][transform_id] = merge_task

    def _build_transform_matrix(self, matrix, is_initial):
        for tool, cmd in matrix["data_transform_order"]:
            self._load_transform(tool, cmd, matrix)
            if "partition_transform" in matrix and is_initial is True:
                partition_task = self._create_partition_task()
                matrix["partition_task"] = partition_task

            transform_tasks = self._create_transform_tasks(is_initial)
            is_initial = False
            matrix["transform_tasks"].append(transform_tasks)
        return matrix

    def _create_merge_task(self, from_tool, from_cmd, merge_tool=None, merge_cmd=None):
        from_tool_cmd = "{}_{}".format(from_tool, from_cmd)
        merge_tool_cmd = "{}_{}".format(merge_tool, merge_cmd)
        save_path = os.path.join(self.save_path, merge_tool)
        if os.path.exists(save_path) is False:
            os.mkdir(save_path)

        merge_key = function_keys[]

        merge_fn = self.func_handler[merge_tool_cmd][from_tool_cmd]
        merge_kwargs = self.kwargs_handler[merge_tool_cmd][from_tool_cmd]

        merge_task = MergeFileData(merge_fn=merge_fn, fn_kwargs=merge_kwargs, save_path=save_path)
        return merge_task

    def _create_partition_task(self):
        partition_task_id = 'data_partition_{}'.format(self.transform_id)

        partition_strategy_fn = self.partition_strategy_handler[self.input_type]
        batch_size, partitions, structure = partition_strategy_fn(self.inputs, self.partitions, self.batch_size)
        self.num_batches = partitions

        if self.prev_tool is None and self.prev_command is None:
            prev_transform_id = "no_prev"
        else:
            prev_transform_id = "{}_{}".format(self.prev_tool, self.prev_command)

        partition_fn = self.func_handler[self.transform_id][prev_transform_id]

        partition_task = PartitionFileData(inputs=self.inputs,
                                           batch_size=batch_size,
                                           partition_fn=partition_fn,
                                           structure=structure,
                                           name=partition_task_id,
                                           slug=partition_task_id)
        return partition_task

    def _create_transform_tasks(self, is_initial):
        if self.prev_transform_id is None:
            prev_id = 'no_prev'
        else:
            prev_id = self.prev_transform_id
        extract_fn = self.func_handler[self.transform_id][prev_id]
        extract_kwargs = self.kwargs_handler[self.transform_id][prev_id]
        dt = DataTransform(task_id=self.transform_id,
                           extract_fn=extract_fn,
                           extract_kwargs=extract_kwargs,
                           template=self.command_template,
                           task_type=self.task_type,
                           **self.task_kwargs
                           )
        dt_tasks = dt.create_tasks(self.num_batches, is_initial)
        return dt_tasks

    def build_pipeline(self):
        for matrix_id in self.pipeline_order:
            matrix = self.pipeline_order[matrix_id]
            if "partition_transform" in matrix:
                partition_result = self._get_partition_result(matrix["partition_task"])
                matrix["partition_transform"]["result"] = partition_result

            num_transforms = len(matrix["data_transform_order"])
            num_batches = matrix["num_batches"]
            transform_result_matrix = [[] for i in range(num_transforms)]
            for x in range(num_batches):
                is_initial = True

                for y, tasks in enumerate(matrix["transform_tasks"]):
                    if is_initial:
                        input_data = partition_result
                    task = tasks[x]
                    #transform_id = "_".format(tool, command)

                    transform_result = self._get_transform_results(task, input_data)
                    transform_result_matrix[y].append(transform_result)
                    input_data = transform_result
                    is_initial = False

            if "transform_results" not in matrix:
                matrix["transform_results"] = transform_result_matrix

            for index, tool_cmd in matrix["merge_transforms"].items():
                transform_id = "{}_{}".format(tool_cmd[0], tool_cmd[1])
                if len(tool_cmd) == 1:
                    continue
                merge_result = self._get_merge_result(matrix["merge_tasks"][transform_id], transform_result_matrix[index])

    def _get_merge_result(self, merge_task, transform_results):
        with self._pipeline as flow:
            merge_result = merge_task(inputs=transform_results)
        return merge_result

    def _get_partition_result(self, partition_task):
        with self._pipeline as flow:
            partition_result = partition_task(inputs=self.inputs)
        return partition_result

    def _get_transform_results(self, transform_task, input_data):
        with self._pipeline as flow:
            result = transform_task(data=input_data)
        return result

    def _load_transform(self, tool, command, matrix):
        if tool not in self.pipe_specs or command not in self.pipe_specs[tool]["commands"]:
            raise Exception("The tool and command you entered does not match the pipe_spec")

        transform_info = {}

        if self.tool and self.command:
            self.prev_tool = self.tool
            transform_info['prev_tool'] = self.prev_tool
            self.prev_command = self.command
            transform_info['prev_command'] = self.prev_command
            self.prev_transform_id = self.transform_id
            transform_info['prev_transform_id'] = self.prev_transform_id

        self.input_type = matrix["input_data"]["type"]
        self.tool = tool
        self.command = command
        transform_info['command'] = self.command
        self.transform_id = "{}_{}".format(self.tool, self.command)
        transform_info['transform_id'] = self.transform_id

        transform_info['save_path'] = self.save_path
        try:
            self.batch_size = matrix["partition_transform"]['batch_size']

        except:
            self.batch_size = None
        transform_info['batch_size'] = self.batch_size
        try:
            self.partitions = matrix["partition_transform"]['partitions']
        except:
            self.partitions = None
        transform_info['partitions'] = self.partitions
        self.command_template = self.pipe_specs[tool]['commands'][command]['template']
        transform_info['command_template'] = self.command_template
        self.task_type = self.pipe_specs[self.tool]['task_type']
        transform_info['task_type'] = self.task_type
        #self.merge = self.pipe_specs[tool]['commands'][command]['merge']
        self.task_kwargs = self.pipe_specs[self.tool]['task_kwargs']

        if "data_transforms" not in matrix:
            matrix = matrix["data_transforms"] = {}
        matrix["data_transforms"][self.transform_id] = transform_info

        return

if __name__ == '__main__':
    y = {1: 'a'}
    t = y[2] = []
    print(t)
    print(y)
