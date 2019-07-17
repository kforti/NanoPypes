import math
import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
import shutil

from prefect import Flow, Task, task

from nanopypes.utilities import CommandBuilder
from nanopypes.pipes.base2 import Pipe
from nanopypes.tasks.partition_data import DataPartitioner, ONTFastqSequenceData


@task
def get_inputs(results):
    print("RESULTS: ", results)
    all_inputs = []
    for batch in results:
        all_inputs.append([i['save'] for i in batch])
    return all_inputs


@task
def get_commands(command_data, template):
    print("COMMAND DATA: ", command_data)
    cb = CommandBuilder(template)
    all_commands = []
    for batch in command_data:
        batch_data = []
        for data in batch:
            #print(data)
            cmd = cb.build_command(data)
            batch_data.append(cmd)
        all_commands.append(batch_data)
    return all_commands


class PipelineBuilder:


    def __init__(self, input_path, pipeline_order, pipeline_name, num_batches, pipe_specs):
        self.pipe_specs = pipe_specs
        self.num_batches = num_batches
        self.pipeline_order = pipeline_order

        self.inputs = [input_path]
        self.tool = None
        self.command = None
        self.save_path = None
        self.data_type = None
        self.partition_strategy = None
        self.command_template = None
        self.save_batches = []
        self._pipeline = Flow(name=pipeline_name)
        self.data_provenance = []



    @property
    def pipeline(self):
        return self._pipeline

    def build_pipeline(self):
        for tool, command in self.pipeline_order:
            print(tool, command)
            self.pipeline_data.load_transform(tool, command)
            self._pipeline = self.pipeline_data.partition_data(self._pipeline)
            #self._pipeline = self.pipeline_data.build_commands(self._pipeline)
            #self._pipeline = self.pipeline_data.pipe_data(self._pipeline)

        #self._pipeline = self.pipeline_data.merge_data(self._pipeline, merge=True)

    def load_transform(self, tool, command):
        if tool not in self.pipe_specs or command not in self.pipe_specs[tool]["commands"]:
            raise Exception("The tool and command you entered does not match the pipe_spec")
        self.tool = tool
        self.command = command
        self.save_path = self.pipe_specs[tool]["save_path"]
        self.data_type = self.pipe_specs[tool]['data_type']
        self.partition_strategy = self.pipe_specs['tool']['commands'][command]['partition']
        self.command_template = self.pipe_specs['tool']['commands'][command]['template']
        # self.transform_ticket['input_data']['data_type'] = self.data_type
        # self.transform_ticket.update(transform={'tool': tool, 'command': command})
        # self.transform_ticket.update(save_data={'save_path': save_path, 'data_type': None})

        return

    def partition_data(self, merge=False):
        """ Split/merge data"""

        # if self.tool is None or self.command is None:
        #     raise Exception("Load a valid transform before partitioning data")

        # This is a task
        demultiplex = False
        partitions = 4
        if self.tool == 'minimap' and self.data_provenance[-1]['transform']['tool'] == 'porechop':
            demultiplex = True

        task_id = 'data_partition_{}'.format(self.data_type)
        data_partitioner = DataPartitioner(inputs=self.inputs,
                                           save_path=self.save_path,
                                           data_type=self.data_type,
                                           pipeline=self._pipeline,
                                           dependencies=self.current_dependencies,
                                           partition_strategy=self.partition_strategy,
                                           name=task_id,
                                           demultiplex=demultiplex,
                                           merge=merge,
                                           slug=task_id)

        data_partitioner.partition_data()
        if self.data_provenance != []:
            results.set_upstream(self.data_provenance[-1]['pipe_tasks'])

        self.inputs = results[2]
        self.transform_ticket['partition']['command_data'] = results[0]
        self.transform_ticket['partition']['inputs'] = results[1]
        self.transform_ticket['partition']['saves'] = results[2]
        self.current_dependencies = results
        batches = []
        for i in range(partitions):
            batches.append(self.inputs[i])

        return pipeline

    def build_commands(self, pipeline):
        """ Create a task that will build a list of commands from partitioned data. Assumes that the data has already been partitioned."""

        template = self.pipe_specs[self.tool]["commands"][self.command]
        command_data = self.transform_ticket['partition']['command_data']
        with pipeline as flow:
            #for i in range(self.num_batches):
            commands = get_commands(command_data,
                                    template)
        self.current_dependencies = commands
        self.transform_ticket['commands'] = commands

        return pipeline

    def pipe_data(self, pipeline):

        pipe = Pipe(commands=self.transform_ticket['commands'],
                    task_id=self.tool,
                    task_type=self.pipe_specs[self.tool]['task_type'],
                    dependencies=self.current_dependencies,
                    pipeline=pipeline,
                    **self.pipe_specs[self.tool]['task_kwargs'])
        pipeline, pipe_tasks = pipe.create_tasks(self.num_batches)
        self.current_dependencies = pipe_tasks
        self.transform_ticket['pipe_tasks'] = pipe_tasks
        self.data_provenance.append(self.transform_ticket)
        return pipeline

    def merge_data(self, pipeline):
        """ Merges the final output data in the last step of the pipeline."""
        return pipeline

    def _create_transform_ticket(self):
        transform_ticket = dict(input_data={'input_path': None, 'data_type': None},
                                             partition={'command_data': None,
                                                        'inputs': None,
                                                        'saves': None},
                                             transform={'tool': None,
                                                        'command': None},
                                             save_data={'save_path': None,
                                                        'data_type': None},
                                             commands=None,
                                             pipe_tasks=None)
        self.data_provenance.append(transform_ticket)


class DataPartitioner:
    data_handler = {'ont_raw_signal': ONTSequenceData,
                    'ont_fastq_seq': ONTFastqSequenceData}
    def __init__(self, save_path, inputs, data_type, pipeline,
                 partition_strategy=None, dependencies=None,
                 merge=False, **task_kwargs):
        self.input_batches = inputs
        self.save_path = save_path
        self.partition_strategy = partition_strategy
        self.dependencies = dependencies
        self.merge = merge
        self.task_kwargs = task_kwargs
        self.data_task = self.data_handler[data_type]
        self.pipeline = pipeline

    def partition_data(self):
        if self.partition_strategy['split'] == 'one_to_one':
            pass
        elif self.partition_strategy['split'] == 'one_to_many':
            pass
        elif self.partition_strategy['split'] == 'many_to_one':
            pass

    def _one_to_one(self, fn):
        inputs = []
        saves = []
        with self.pipeline as flow:
            for batch in self.input_batches:
                partition_task = self.data_task(save_path=self.save_path,
                                                dependencies=self.dependencies,
                                                inputs=batch,
                                                merge=self.merge,
                                                **self.task_kwargs)
                result = partition_task()




if __name__ == '__main__':
    from prefect import Flow

    inputs = [['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/9', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/0', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/7'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/6', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/8'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/4', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/3', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/2'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/5']]
    from nanopypes.pipes.base2 import PrintCommands

    flow = Flow('test-flow')
    template = "minimap2 -ax splice /path/to/reference {input} -o {save}"
    data = ONTFastqSequenceData(inputs=inputs,
                                save_path="some/save/path/",
                                dependencies=[],
                                partitions=4,
                                name='task_test',
                                )
    cmds = PrintCommands()
    with flow as f:
        results = data()
        commands = get_commands(results, template)
        cmds(commands)

    flow.run()
