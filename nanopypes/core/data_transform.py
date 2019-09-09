from nanopypes.tasks import PullImage, BatchSingularityExecute
from nanopypes.tasks.transform_task import ShellTransformTask

from datetime import timedelta
import os

from prefect import Task


class PrintCommands(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, commands):
        print("SLUG: ", self.slug, "\nCOMMANDS: ", commands, "\n\n")

class Transform():
    task_handler = {'singularity': BatchSingularityExecute,
                    'shell': ShellTransformTask,
                    'print_commands': PrintCommands}

    def __init__(self, task_id, save_path, task_type, template, **task_kwargs):
        self.task_type = task_type
        self.save_path = save_path
        self.task = self.task_handler[self.task_type]
        self.task_id = task_id
        self.template = template
        self.task_kwargs = task_kwargs

        self.all_tasks = []

class MergeTransform(Transform):

    def __init__(self, merge_fn, **kwargs):
        super().__init__(**kwargs)
        self.merge_fn = merge_fn

        self.all_tasks = []

    def create_tasks(self):
        save_path = os.path.join(self.save_path, self.task_id)
        if os.path.exists(save_path) is False:
            os.mkdir(save_path)
        task = self.task(template=self.template, save_path=save_path, extract_fn=self.merge_fn,
                         slug=self.task_id, name=self.task_id, max_retries=3, retry_delay=timedelta(seconds=1),
                         **self.task_kwargs)
        return task

class DataTransform(Transform):

    def __init__(self, extract_fn, **kwargs):
        super().__init__(**kwargs)
        self.extract_fn = extract_fn

        self.all_tasks = []

    def create_tasks(self, num_batches, is_initial):
        save_path = os.path.join(self.save_path, self.task_id)
        if os.path.exists(save_path) is False:
            os.mkdir(save_path)
        for i in range(num_batches):
            task_id = self.task_id + "_batch_{}".format(str(i))
            batch_save_path = os.path.join(save_path, "batch_{}".format(str(i)))
            if os.path.exists(batch_save_path) is False:
                os.mkdir(batch_save_path)
            task = self.task(template=self.template, save_path=batch_save_path, batch_num=i, extract_fn=self.extract_fn, slug=task_id, name=task_id, max_retries=3, retry_delay=timedelta(seconds=1), is_initial=is_initial, **self.task_kwargs)

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

