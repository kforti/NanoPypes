from nanopypes.tasks import SingularityTask, LSFJob, ShellTask
from nanopypes.utilities import InValidTaskError, CommandBuilder

import os


class Pipeline:
    def __init__(self, pipes):
        self.pipes = pipes

    def __call__(self):
        for pipe in self.pipes:
            pipe()


class Pipe():
    task_handler = {'singularity': SingularityTask,
                    'shell': ShellTask}

    def __init__(self, input_paths, command_config,
                 commands, pipeline, save_path, dependencies=None, task_config=None):
        self._expected_data = None
        self.input_paths = input_paths
        self.save_path =save_path
        self.command_config = command_config
        self.commands = commands
        self.pipeline = pipeline
        self.dependencies = dependencies
        self.task_config = task_config
        self.task_type = self.task_config.pop("task_type")
        self.task = self.task_handler[self.task_type]

        self.command_builder = CommandBuilder(self.commands, self.command_config)

        self.save_paths = []
        self._generate_save_paths()
        self._expected_data = []
        self.all_tasks = []
        self._all_commands = {}

    @property
    def all_commands(self):
        return self._all_commands

    def execute(self):
        pass

    @classmethod
    def from_dict(cls, config_dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        return instance

    def __call__(self):
        return self.execute()

    @property
    def expected_data(self):
        return self.save_paths, self.all_tasks

    def create_tasks(self):
        pass

    def _generate_save_paths(self):
        pass



