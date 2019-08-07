from prefect import task, Task, Flow
from prefect.utilities.tasks import defaults_from_attrs

from nanopypes.utilities import CommandBuilder
from nanopypes.pipes.base2 import Pipe
from nanopypes.distributed_data.partition_data import DataPartitioner, ONTFastqSequenceData



def run_pipeline(pipeline, **kwargs):
    """

    :param pipeline:
    :param kwargs:
    :return:
    """
    state = pipeline.run(**kwargs)
    if state.is_failed():
        pass


@task
def get_inputs(results):
    print("RESULTS: ", results)
    all_inputs = []
    for batch in results:
        all_inputs.append([i['save'] for i in batch])
    return all_inputs



class BuildCommands(Task):

    def __init__(self, command_data=None, template=None, **kwargs):
        super().__init__(**kwargs)
        self.command_data = command_data
        self.template = template

    @defaults_from_attrs('command_data', 'template')
    def run(self, command_data=None, template=None):
        print("COMMAND DATA: ", command_data)
        cb = CommandBuilder(template)
        all_commands = []
        # for batch in command_data:
        #     batch_data = []
        for data in command_data:
            #print(data)
            cmd = cb.build_command(data)
            #batch_data.append(cmd)
            all_commands.append(cmd)
        #all_commands.append(batch_data)
        return all_commands


class PipelineBuilder:

    def __init__(self, inputs, pipeline_order,
                 pipeline_name, num_batches, pipe_specs):
        self.pipe_specs = pipe_specs
        self.num_batches = num_batches
        self.pipeline_order = pipeline_order
        self.inputs = inputs

        self._pipeline = Flow(name=pipeline_name)
        self.tool = None
        self.command = None
        self.save_path = None
        self.data_type = None
        self.partition_strategy = None
        self.command_template = None
        self.data_provenance = []
        self.pipe_results = None

    @property
    def pipeline(self):
        return self._pipeline

    def build_pipeline(self):
        transform_order = [(self.partition_tasks), (self.command_tasks), (self.pipe_tasks)]

        for transform in self.data_provenance:
            self._build_transform(transform)



    def _build_transform(self, transform):
        # inputs = self.inputs
        partition_results, command_results, pipe_results, curr_dependencies, next_inputs = [], [], [], [], []
        print("partition_tasks ", transform['partition_tasks'])
        print(transform['num_partitions'])
        with self.pipeline as flow:
            for i, task in enumerate(transform['partition_tasks']):
                if transform['merge']:
                    result = task(self.inputs)
                    if self.pipe_results:
                        result.set_upstream(self.pipe_results)
                else:
                    result = task(self.inputs[i])

                    if self.pipe_results:
                        result.set_upstream(self.pipe_results[i])

                if transform['num_partitions'] > 0:
                    for i in range(transform['num_partitions']):
                        partition_results.append(result['command_data'][i])
                        next_inputs.append(result['saves'][i])
                else:
                    partition_results.append(result['command_data'])
                    next_inputs.append(result['saves'])
            print(transform['command_tasks'])
            for i, task in enumerate(transform['command_tasks']):
                result = task(partition_results[i])
                command_results.append(result)
            for i, task in enumerate(transform['pipe_tasks']):
                if self.pipe_results:
                    result = task(command_results[i])
                    #result.set_upstream(self.pipe_results[i])
                else:
                    result = task(command_results[i])
                pipe_results.append(result)

            self.pipe_results = pipe_results
            self.inputs = next_inputs
            print("inputs: ", self.inputs)


    def build_tasks(self):
        for tool, command in self.pipeline_order:
            print(tool, command)
            self._load_transform(tool, command)
            self._partition_data()
            self._build_commands()
            self._pipe_data()
            self._create_transform_ticket()

    def _load_transform(self, tool, command):
        if tool not in self.pipe_specs or command not in self.pipe_specs[tool]["commands"]:
            raise Exception("The tool and command you entered does not match the pipe_spec")
        self.tool = tool
        self.command = command
        self.save_path = self.pipe_specs[tool]["save_path"]
        self.data_type = self.pipe_specs[tool]['data_type']
        partitions = self.pipe_specs[tool]['commands'][command]['partitions']
        self.partitions = partitions
        self.partition_strategy = self.pipe_specs[tool]['commands'][command]['split_merge']
        self.command_template = self.pipe_specs[tool]['commands'][command]['template']
        self.merge = self.pipe_specs[tool]['commands'][command]['merge']

        self.command_tasks = []
        self.pipe_tasks = []
        self.partition_tasks = []
        self.save_batches = []

        return

    def _partition_data(self):
        """ Split/merge data"""
        if self.partitions != 0 and self.partitions < self.num_batches:
            self.num_batches = self.partitions

        task_id = 'data_partition_{}'.format(self.data_type)
        data_partitioner = DataPartitioner(num_batches=self.num_batches,
                                           save_path=self.save_path,
                                           data_type=self.data_type,
                                           partitions=self.partitions,
                                           partition_strategy=self.partition_strategy,
                                           name=task_id,
                                           slug=task_id,
                                           )

        self.partition_tasks = data_partitioner.partition_data()

        if self.partitions != 0:
            self.num_batches = self.partitions

    def _build_commands(self):
        """ Create a task that will build a list of commands from partitioned data. Assumes that the data has already been partitioned."""

        template = self.pipe_specs[self.tool]["commands"][self.command]['template']
        print('num_batches ', self.num_batches)
        for i in range(self.num_batches):
            commands = BuildCommands(template=template)
            self.command_tasks.append(commands)

    def _pipe_data(self):
        task_id = "_".join([self.tool, self.command])
        pipe = Pipe(task_id=task_id,
                    task_type=self.pipe_specs[self.tool]['task_type'],
                    **self.pipe_specs[self.tool]['task_kwargs'])
        self.pipe_tasks = pipe.create_tasks(self.num_batches)

    def merge_data(self):
        """ Merges the final output data in the last step of the pipeline."""
        return

    def _create_transform_ticket(self):
        transform_ticket = dict(input_data={'inputs': self.inputs, 'data_type': self.data_type},
                                partition_tasks=self.partition_tasks,
                                transform={'tool': self.tool,
                                           'command': self.command},
                                save_data={'save_path': self.save_path,
                                           'data_type': None},
                                command_tasks=self.command_tasks,
                                pipe_tasks=self.pipe_tasks,
                                num_partitions=self.partitions,
                                merge=self.merge)
        self.data_provenance.append(transform_ticket)




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
