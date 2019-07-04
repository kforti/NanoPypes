import os

from nanopypes.pipes.base import Pipe
from nanopypes.utilities import InValidTaskError, CommandBuilder


class AlbacoreBasecaller(Pipe):

    def __init__(self, input_paths, save_path, pipe_config, commands, pipeline, dependencies):
        self.input_paths = input_paths
        self.save_path = save_path
        self.pipe_config = pipe_config
        self.commands = commands
        self.pipeline = pipeline

        self.task_type = pipe_config["task"]
        self.task = self.task_handler[self.task_type]

        self.command_builder = CommandBuilder(self.commands, self.pipe_config["commands"])

        self.save_paths = []
        self._generate_save_paths()
        self._expected_data = []

    @property
    def expected_data(self):
        return self.save_paths

    def create_tasks(self):
        command_id = self.commands[0]
        all_tasks = []
        for i in range(len(self.input_paths)):
            command = self.command_builder.build_command(command_id,
                                                         input=self.input_paths[i],
                                                         save_path=self.save_paths[i])
            if self.task_type == 'shell':
                task = self.task(command, slug=(command_id + os.path.basename(self.input_paths[i])))
                all_tasks.append(task)

        with self.pipeline as flow:
            for i in range(len(all_tasks)):
                result = all_tasks[i]()
                self._expected_data.append((result, self.save_paths[i]))

    def _generate_save_paths(self):
        import os
        for path in self.input_paths:
            self.save_paths.append(os.path.join(self.save_path, os.path.basename(path)))


if __name__ == '__main__':
    from nanopypes.pipelines.variant_caller import get_config
    from prefect import Flow
    from prefect.engine.executors import DaskExecutor
    from distributed import LocalCluster

    cluster = LocalCluster()

    pipeline = Flow("pipeline")
    executor = DaskExecutor(address=cluster.scheduler_address)

    input_paths = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/0",
                   "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/1",
                   "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/3",
                   ]
    save_path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_test"

    pipeline = Flow("basecall_pipeline")
    commands = ["basecall"]
    config = get_config([("albacore", "basecall")])
    print(config)
    # c = "read_fast5_basecaller.py  --input {input} --save_path {save_path} --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fastq --worker_threads 1 --reads_per_fastq 1000 "
    # print(c.format_map({'input': 'here is input', 'save_path': 'here is save path'}))
    albacore = AlbacoreBasecaller(input_paths, save_path, config["albacore"], commands, pipeline)
    albacore.create_tasks()
    p = albacore.pipeline
    print(p.tasks)
    p.run(executor=executor)




