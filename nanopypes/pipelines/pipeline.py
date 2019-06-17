from collections import defaultdict


class Pipeline:
    """Pipeline object is used to store tasks, task names and the data
    and dependencies associated with those tasks. The object should first
    be instantiated and attributes added through the add_* methods.
    """
    def __init__(self, tasks=None, data=None,
                 dependencies=None, task_order=None,
                 dag_dict=None):
        self._tasks = tasks or {}
        self._data = data or {}
        self._dependencies = dependencies or defaultdict(set)
        self._task_order = task_order or []

        if dag_dict:
            self._build_pipeline(dag_dict)

    def _build_from_dict(self, dag):
        for task, task_dict in dag.items():
            self.add_task(task, task_dict['task_handle'])
            self.add_dependencies(task, task_dict['dependencies'])
            self.add_data(task, task_dict['data'])

    def add_task(self, task_name, task, *args):
        """
        Adds a task or a list of tasks to the pipeline.

        Args:
            - task_name (string): a name to refer to this task by.
            - task (Task): 'Task' object
            - *args (list): a list of tuples containing (task name, Task object)
        """
        task_dict = {'task_handle': task,
                     'yielded': False}
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

    def _build_data_graph(self):
        connections = []
        for task, dependencies in self.dependencies.items():
            for i in dependencies:
                connections.append((task, i))

    def __iter__(self):
        for task in self._tasks:
            if self._tasks[task]['yielded'] == True:
                continue
            elif task not in self._dependencies:
                yield task
                self._tasks[task]['yielded'] = True
            else:
                for dependency in self._dependencies[task]:
                    if self._tasks[dependency]['yielded'] == False:
                        break
                yield task
                self._tasks[task]['yielded'] = True

def command_factory(command_builder, data, builder_key=None):
    if builder_key:
        return builder_key()
    commands = []
    for i in data:
        command_builder

class PipelineFactory:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def create_tasks(self, task, task_dependencies, task_kwrgs):
        for kwrgs in task_kwrgs:
            self.pipeline.add_task(task(kwrgs))




if __name__ == '__main__':
    dag = {'task1': {'data':[]}}
    p = Pipeline()

    print(p.dependencies)
    for task in p:
        print(task)
