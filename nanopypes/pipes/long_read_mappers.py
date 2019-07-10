import os


from nanopypes.pipes.base import Pipe



class MiniMap2(Pipe):
    commands = {'genomic': 'minimap2 -ax map-ont %(ref)s %(read)s -o %(output)s',
                'splice': 'minimap2 -ax splice %(ref)s %(read)s > %(output)s',
                'rna': 'minimap2 -ax splice -uf -k14 %(ref)s %(read)s -o %(output)s',
                'overlap': 'minimap2 -x ava-ont %(ref)s %(read)s -o %(output)s'}

    def __init__(self, reference, **kwargs):
        super().__init__(**kwargs)
        self.reference = reference
        self.task_id = "minimap2"

    def create_tasks(self):
        command_id = self.commands[0]
        self._all_commands[command_id] = []

        for i in range(len(self.input_paths)):
            command = self.command_builder.build_command(command_id,
                                                         reference=self.reference,
                                                         read=self.input_paths[i],
                                                         save_path=self.save_paths[i])
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
        import re
        for path in self.input_paths:
            pass_reads_path = os.path.join(path, "workspace", "pass")
            for fastq in os.listdir(pass_reads_path):
                samfile_name = re.sub(r'[\.].+', '.sam', fastq)
                self.save_paths.append(os.path.join(self.save_path, samfile_name))







