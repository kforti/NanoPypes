import os

from nanopypes.pipes.base import Pipe



class Porechop(Pipe):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_id = "porechop"

    def create_tasks(self):
        command_id = self.commands[0]
        self._all_commands[command_id] = []

        for i in range(len(self.input_paths)):
            command = self.command_builder.build_command(command_id,
                                                         input_dir=self.input_paths[i],
                                                         save_dir=self.save_paths[i])
            self._all_commands[command_id].append(command)
            task_id = self.task_id + "_" + os.path.basename(self.input_paths[i])
            task = self.task(command, slug=task_id, name=self.task_id, **self.task_config)
            if self.dependencies:
                task.set_upstream(self.dependencies[i], flow=self.pipeline)
            else:
                self.pipeline.add_task(task)

            self.all_tasks.append(task)

        return self.pipeline

    def _generate_save_paths(self):
        for i, path in enumerate(self.input_paths):
            self.input_paths[i] = os.path.join(path, "workspace", "path")
            self.save_paths.append(os.path.join(self.save_path, os.path.basename(path)))





