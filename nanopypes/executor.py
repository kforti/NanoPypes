from distributed import as_completed





class Executor:
    def __init__(self, cluster_manager=None, pipeline=None, command_template=None):
        self.cluster_manager = cluster_manager
        self.pipeline = pipeline
        self.command_template = command_template
        self.client = cluster_manager.client

        self.dispatched_tasks = 0
        self.completed_tasks = None
        self.futures = []

    @property
    def cluster_full(self):
        if self.cluster_manager.connected_workers == self.dispatched_tasks:
            return True
        return False

    def execute(self):
        """"""
        pass
    def terminate(self):
        """"""
        pass


class EagerExecutor(Executor):
    """"""
    def execute(self):
        for task in self.pipeline:
            future = self.client.submit(task.run())
            self.dispatched_tasks += 1

            if self.cluster_full is False and self.completed_tasks is None:
                self.futures.append(future)

            if self.cluster_full and self.completed_tasks:
                completed_future = next(self.completed_tasks)
                self.completed_tasks.add(future)
                self.dispatched_tasks -= 1

            elif self.cluster_full and self.completed_tasks is None:
                self.completed_tasks = as_completed(self.futures)

        self.terminate()

    def terminate(self):
        self.client.gather(self.completed_tasks)



if __name__ == '__main__':
    from nanopypes import ClusterManager, Pipeline, CommandBuilder

    COMMAND_TEMPLATE = ""

    pipeline = Pipeline

    cluster_manager = ClusterManager







