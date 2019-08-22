from prefect import Task, Flow, task
from prefect.utilities.tasks import defaults_from_attrs



class PartitionFileData(Task):

    def __init__(self, inputs=None, structure=None, partition_fn=None, fn_kwargs={}, batch_size=None, **kwargs):
        super().__init__(**kwargs)
        self.partition_fn = partition_fn
        self.structure = structure
        self.fn_kwargs = fn_kwargs
        self.batch_size = batch_size
        self.inputs = inputs

    @defaults_from_attrs('inputs', 'structure', 'partition_fn', 'fn_kwargs', 'batch_size')
    def run(self, inputs=None, structure=None, partition_fn=None, batch_size=None, fn_kwargs={}):

        results = partition_fn(input_path=inputs, structure=structure, batch_size=batch_size, **fn_kwargs)

        return results


class MergeFileData(Task):
    def __init__(self, inputs=None, merge_fn=None, save_path=None, fn_kwargs={}, **kwargs):
        super().__init__(**kwargs)
        self.merge_fn = merge_fn
        self.fn_kwargs = fn_kwargs
        self.save_path = save_path

        self.inputs = inputs
    @defaults_from_attrs('inputs', 'save_path', 'merge_fn', 'fn_kwargs')
    def run(self, inputs=None, save_path=None, merge_fn=None,  fn_kwargs={}):
        results = merge_fn(inputs=inputs, save_path=save_path, **fn_kwargs)

        return results


if __name__ == '__main__':
    y = {1: ["a", "b"],
         2: ["c", "d"]}
    for num, let1, let2 in y.items():
        print(num, let1, let2)
