import math
import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
import shutil

from prefect import Task, task

from nanopypes.utilities import CommandBuilder
from nanopypes.pipes.base2 import Pipe
from nanopypes.tasks.partition_data import ONTSequenceData, ONTFastqSequenceData, ONTDemultiplexedData


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


class PipelineData:
    data_handler = {'ont_raw_signal': ONTSequenceData,
                    'ont_fastq_seq': ONTFastqSequenceData}

    def __init__(self, input_path, cluster_manager, pipe_specs):
        self.pipe_specs = pipe_specs
        self.cluster_manager = cluster_manager
        self.num_batches = 4
        self.inputs = [input_path]
        self.data_type = None
        self.data = None
        self.tool = None
        self.command = None
        self.data_provenance = []
        self.current_dependencies = None

    def load_transform(self, tool, command):
        if tool not in self.pipe_specs or command not in self.pipe_specs[tool]["commands"]:
            raise Exception("The tool and command you entered does not match the pipe_spec")
        self.tool = tool
        self.command = command
        self.save_path = self.pipe_specs[tool]["save_path"]
        self.data_type = self.pipe_specs[self.tool]['data_type']
        self.data = self.data_handler[self.data_type]
        self.transform_ticket = dict(input_data={'input_path': None, 'data_type': self.data_type},
                                     partition={'command_data': None,
                                                'inputs': None,
                                                'saves': None},
                                     transform={'tool': self.tool,
                                                'command': self.command},
                                     save_data={'save_path': self.save_path,
                                                'data_type': None},
                                     commands=None,
                                     pipe_tasks=None)
        return

    def partition_data(self, pipeline, merge=False):
        """ Split/merge data"""

        if self.tool is None or self.command is None:
            raise Exception("Load a valid transform before partitioning data")

        # This is a task
        demultiplex = False
        partitions = 4
        #if self.tool == 'albacore':
         #   partitions = 4#(self.cluster_manager.num_workers * 2)
        if self.tool == 'minimap' and self.data_provenance[-1]['transform']['tool'] == 'porechop':
            demultiplex = True

        task_id = 'data_partition_{}'.format(self.data_type)
        with pipeline as flow:
            data = self.data(
                             save_path=self.save_path,
                             dependencies=self.current_dependencies,
                             partitions=partitions,
                             name=task_id,
                             demultiplex=demultiplex,
                             merge=merge,
                             slug=task_id)

            results = data(inputs=self.inputs)
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




if __name__ == '__main__':
    from prefect import Flow

    inputs = [['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/9', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/0', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/7'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/6', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/8'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/4', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/3', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/2'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/5']]
    from nanopypes.pipes.base2 import PrintCommands

    flow = Flow('test-flow')
    template = "minimap2 -ax splice /path/to/reference {input} -o {save}"

    with flow as f:

        data = ONTFastqSequenceData(inputs=inputs,
                                 save_path="some/save/path/",
                                 dependencies=[],
                                 partitions=4,
                                 name='task_test',
                                 )
        cmds = PrintCommands()

        results = data()
        commands = get_commands(results, template)
        cmds(commands)

    flow.run()
