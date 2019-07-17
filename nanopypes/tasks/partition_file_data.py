from prefect import Task, Flow, task
from prefect.utilities.tasks import defaults_from_attrs


class PartitionBatch(Task):

    def __init__(self, batch=None, input_fn=None, save_fn=None, **kwargs):
        super().__init__(**kwargs)
        self.batch = batch
        self.input_fn = input_fn
        self.save_fn = save_fn

    @defaults_from_attrs('batch', 'input_fn', 'save_fn')
    def run(self, batch=None, input_fn=None, save_fn=None):
        inputs = []
        saves = []
        command_data = []
        for directory in batch:
            input_result = input_fn(directory)
            save_result = save_fn(directory)
            command_data.append({'input': input_result, 'save': save_result})
            inputs.append(input_result)
            saves.append(save_result)

        return {'inputs': inputs, 'saves': saves, 'command_data': command_data}

import os
def get_contents(path):
    return os.listdir(path)

def get_name(path):
    return os.path.basename(path)

@task
def print_result(result):
    print(result)

if __name__ == '__main__':
    flow = Flow('data-partition')

    batch = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/0",
             "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/1",
             "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/3"]

    task = PartitionBatch(batch, get_contents, get_name)

    with flow as f:
        results = task()
        a = results['input']
        b = results['save']
        print_result(a)
        print_result(b)

    flow.run()
    print(a, b)

