from nanopypes.tasks import SingularityTask, BatchShellTask

from prefect import Task
from prefect.tasks.shell import ShellTask

class PrintCommands(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, commands):
        print("SLUG: ", self.slug, "\nCOMMANDS: ", commands, "\n\n")


class Pipe():
    task_handler = {'singularity': SingularityTask,
                    'shell': BatchShellTask,
                    'print_commands': PrintCommands}

    def __init__(self, commands, pipeline, task_id, task_type, dependencies=None, **task_kwargs):
        self.commands = commands
        self.pipeline = pipeline
        self.dependencies = dependencies
        self.task_type = task_type
        self.task = self.task_handler[self.task_type]
        self.task_id = task_id
        self.task_kwargs = task_kwargs

        self.all_tasks = []

    def create_tasks(self, num_batches):
        with self.pipeline as flow:
            for i in range(num_batches):
                task_id = self.task_id + "_batch_{}".format(str(i))
                cmds = self.commands[i]
                task = self.task(slug=task_id, name=task_id, **self.task_kwargs)
                results = task(cmds)
                # if self.dependencies:
                #     task.set_upstream(self.dependencies[i], flow=self.pipeline)
                # elif self.dependencies is None:
                #     self.pipeline.add_task(task)

                self.all_tasks.append(task)

        return self.pipeline, self.all_tasks

def my_func(input, save_path, **kwargs):
    print(input)
    print(save_path)
    print(kwargs)

if __name__ == '__main__':
    import math
    import os
    path = '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'
    children = ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/9', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/0', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/7', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/6', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/8', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/4', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/3', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/2', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/5']
    batch_size = 3
    batches = [children[i:i + batch_size] for i in range(0, len(children), batch_size)]
    print(batches)
    #print([os.path.join(path, i) for i in os.listdir(path)])

