from nanopypes.utilities import defaults_from_attrs


class NanoPypesExecutor:
    def __init__(self, cluster_manager=None, task=None, data=None, command_template=None):
        self.cluster_manager = cluster_manager
        self.task = task
        self.data = data
        self.command_template = command_template
        self.client = None

    @defaults_from_attrs
    def execute_eager_strategy(self, cluster_manager=None, pipeline=None,
                                 template_builder=None, expected_workers=None):
        avail_workers = expected_workers or cluster_manager.expected_workers
        if avail_workers == 0:
            raise AttributeError("You must provide expected workers"
                                 ", either through the cluster_manager or expected_workers")

        dispatched_commands = 0




if __name__ == '__main__':
    import re
    d = "hello {world}"
    dl = d.split()





