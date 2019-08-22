from nanopypes.tasks import PullImage, BatchSingularityExecute
from nanopypes.tasks.transform_task import ShellTransformTask

from datetime import timedelta

from prefect import Task


class PrintCommands(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, commands):
        print("SLUG: ", self.slug, "\nCOMMANDS: ", commands, "\n\n")


class DataTransform():
    task_handler = {'singularity': BatchSingularityExecute,
                    'shell': ShellTransformTask,
                    'print_commands': PrintCommands}

    def __init__(self, task_id, task_type, template, extract_fn, extract_kwargs, **task_kwargs):
        self.task_type = task_type
        self.task = self.task_handler[self.task_type]
        self.task_id = task_id
        self.extract_fn = extract_fn
        self.extract_kwargs = extract_kwargs
        self.template = template
        self.task_kwargs = task_kwargs

        self.all_tasks = []

    def create_tasks(self, num_batches, is_initial):
        for i in range(num_batches):
            task_id = self.task_id + "_batch_{}".format(str(i))
            task = self.task(template=self.template, batch_num=i, extract_fn=self.extract_fn, fn_kwargs=self.extract_kwargs, slug=task_id, name=task_id, max_retries=3, retry_delay=timedelta(seconds=1), is_initial=is_initial, **self.task_kwargs)

            self.all_tasks.append(task)

        return self.all_tasks

def my_func(input, save_path, **kwargs):
    print(input)
    print(save_path)
    print(kwargs)

if __name__ == '__main__':
    import math
    import os
    path = '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass'
    children = ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/9', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/0', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/7', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/6', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/8', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/4', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/3', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/2', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/5']
    batch_size = 3
    batches = [children[i:i + batch_size] for i in range(0, len(children), batch_size)]
    print(batches)
    #print([os.path.join(path, i) for i in os.listdir(path)])

