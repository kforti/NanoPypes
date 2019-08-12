from prefect import Task, Flow, task
from prefect.utilities.tasks import defaults_from_attrs


class BatchPartition(Task):

    def __init__(self, batches=None, batch_num=None, input_fn=None, fn_kwargs=None, dependencies=None, partition_num=None, **kwargs):
        super().__init__(**kwargs)
        self.batches = batches
        self.partition_num = partition_num
        self.input_fn = input_fn
        self.fn_kwargs = fn_kwargs
        self.dependencies = dependencies
        self.batch_num = batch_num

    @defaults_from_attrs('batches', 'input_fn', 'fn_kwargs', 'dependencies', 'batch_num', 'partition_num')
    def run(self, batches=None, batch_num=None, partition_num=None, input_fn=None, fn_kwargs=None, dependencies=None):
        inputs = []
        saves = []
        command_data = []
        print("BATCH NUM: ", batch_num, " BATCH CONTENTS: ", batches)

        if partition_num:
            batches = batches["saves"][partition_num]
        elif batch_num:
            batches = batches["saves"]


        results = input_fn(batches, batch_num, **fn_kwargs)
        # command_data.append({'input': input_result, 'save': save_result})
        # inputs.append(input_result)
        # saves.append(save_result)
        print("HERE: ", results[0])
        print("HERE: ", results[1])
        print("HERE: ", results[2])

        return {'inputs': results[1], 'saves': results[2], 'command_data': results[0]}

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

