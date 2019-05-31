from collections import defaultdict


class Pipeline:
    """Pipeline object is used to store tasks, task names and the data
    and dependencies associated with those tasks. The object should first
    be instantiated and attributes added through the add_* methods.
    """
    def __init__(self):
        self._tasks = {}
        self._data = {}
        self._dependencies = defaultdict(set)
        self._task_flows = []

    def add_task(self, task_name, task, *args):
        """
        Adds a task or a list of tasks to the pipeline.

        Args:
            - task_name (string): a name to refer to this task by.
            - task (Task): 'Task' object
            - *args (list): a list of tuples containing (task name, Task object)
        """
        task_dict = {'task_handle': task}
        self._tasks[task_name] = task_dict

    def add_data(self, task_name, data, *args):
        """
        Adds Data object or a list of Data object to the pipeline.
        Task name is also supplied in order to connect the data to a
        specific task.

        Args:
            - task_name (string): a name to connect the Data object to a specific task.
            - data (Data): 'Data' object
            - *args (list): a list of tuples containing (task name, Data object)
        """
        self._data[task_name] = data

    def add_dependencies(self, task_name=None, dependencies=None, *args):
        """
        Adds Data object or a list of Data object to the pipeline.
        Task name is also supplied in order to connect the data to a
        specific task.

        Args:
            - task_name (string): a name to connect the dependencies to a specific task.
            - dependencies (set): a set of strings that repesent the names of the depended upon tasks.
            - *args (list): a list of tuples containing (task name, {dependency task names}),
                where the dependency task names are a set.
        """
        if task_name and dependencies:
            for d in dependencies:
                self._dependencies[task_name].add(d)

        for task_name, dependencies in args:
            for d in dependencies:
                self._dependencies[task_name].add(d)

    @property
    def dependencies(self):
        return self._dependencies

    def get_task(self):
        self._build_data_flow()
        for i in data



if __name__ == '__main__':
    p = Pipeline()
    p.add_data('task1', 'data')
    p.add_task('task1', 'task1')
    p.add_dependencies('task1', ['task2'], ('task2', ['task3']))
    p.dependencies
