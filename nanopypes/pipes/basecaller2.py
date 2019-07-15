import os

from nanopypes.pipes.base import Pipe


class AlbacoreBasecaller(Pipe):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_id = "albacore"

    def create_tasks(self):
        command_id = self.commands[0]
        self._all_commands[command_id] = []

        for i in range(len(self.input_paths)):
            command = self.command_builder.build_command(command_id,
                                                         input=self.input_paths[i],
                                                         save_path=self.save_paths[i])
            self._all_commands[command_id].append(command)
            task_id = self.task_id + "_" + os.path.basename(self.input_paths[i])
            task = self.task(command, slug=task_id, name=self.task_id, **self.task_config)
            if self.dependencies:
                task.set_upstream(self.dependencies[i], flow=self.pipeline)
            else:
                self.pipeline.add_task(task)
            print(vars(task))

            self.all_tasks.append(task)

        return self.pipeline

    def _generate_save_paths(self):
        for path in self.input_paths:
            self.save_paths.append(os.path.join(self.save_path, os.path.basename(path)))


if __name__ == '__main__':
    from nanopypes.pipelines.variant_caller import get_config
    from prefect import Flow
    from prefect.engine.executors import DaskExecutor
    from distributed import LocalCluster

    cluster = LocalCluster()

    pipeline = Flow("local_pipeline.yml")
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
    albacore = AlbacoreBasecaller(input_paths=input_paths,
                                  save_path=save_path,
                                  command_config=config["albacore"],
                                  commands=commands,
                                  pipeline=pipeline,
                                  task_config=config["albacore"]["task_config"])
    albacore.create_tasks()
    print(albacore.expected_data)
    # p = albacore.local_pipeline.yml
    #print(p.tasks)
    # p.run(executor=executor)




