import os


from nanopypes.pipes.base import Pipe



class MiniMap2(Pipe):
    commands = {'genomic': 'minimap2 -ax map-ont %(ref)s %(read)s -o %(output)s',
                'splice': 'minimap2 -ax splice %(ref)s %(read)s > %(output)s',
                'rna': 'minimap2 -ax splice -uf -k14 %(ref)s %(read)s -o %(output)s',
                'overlap': 'minimap2 -x ava-ont %(ref)s %(read)s -o %(output)s'}

    def __init__(self, reference, **kwargs):
        self.ids = kwargs.get('input_paths')
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
            task_id = self.task_id + "_" + os.path.basename(self.ids[i])
            task = self.task(command, slug=task_id, name=self.task_id, **self.task_config)
            if self.dependencies:
                task.set_upstream(self.dependencies[i], flow=self.pipeline)
            else:
                self.pipeline.add_task(task)
            print(vars(task))

            self.all_tasks.append(task)

        return self.pipeline

    def _generate_save_paths(self):
        import re
        from pathlib import Path
        for path_data in self.input_paths:
            if isinstance(path_data, dict):
                batch = path_data[batch]

                # pass_reads_path = os.path.join(path, "workspace", "pass")
                sam_batch = []
                for i, fastq in path_data['paths']:
                    samfile_name = re.sub(r'[\.].+', '_{num}_batch_{batch}.sam'.format(num=str(i), batch=batch), fastq)
                    sam_batch.append(os.path.join(self.save_path, samfile_name))
                self.save_paths.append(sam_batch)






