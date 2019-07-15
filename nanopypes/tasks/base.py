from prefect import Task, task
import os
from pathlib import Path

#
# class Task(Task):
#
#     def __init__(self, name=None, **kwargs):
#         self.name = name
#         super().__init__(**kwargs)
#
#     @classmethod
#     def from_dict(cls, config_dict):
#         instance = cls.__new__(cls)
#         instance.__dict__.update(config_dict)
#         return instance


class GetFastqs(Task):
    def __init__(self, directory, **kwargs):
        super().__init__(**kwargs)
        self.directory = directory
        self.paths_data = {'batch': None,
                           'paths': []}
    def run(self):
        dir_path = Path(self.directory)
        self.paths_data['batch'] = dir_path.name
        dir_path = dir_path.joinpath("workspace", "pass")


        for dir, subdirs, files in os.walk(str(dir_path)):
            for file in files:
                path = Path(dir).joinpath(file)
                if '.fq' in path.suffixes or '.fastq' in path.suffixes:
                    self.paths_data['paths'].append(str(path))
        print('Paths Data: ', self.paths_data)
        return self.paths_data


class CommandBuilder(Task):
    """
    Class for generating command line command strings from a template. Templates are used to generate
    the command across partitioned data (for parallel processing).

    Args:
        - template (string): a string template with variables wrapped in brackets {}.
            (Example template: 'minimap2 -ax map-ont {ref} {read} -o {output}')
    """
    def __init__(self, command_kwargs, template, **kwargs):
        super().__init__(**kwargs)
        self.command_kwargs = command_kwargs
        self.template = template

    def run(self):
        commands = []
        for kwarg in self.command_kwargs:
            commands.append(self.template.format_map(kwarg))
        return commands

    # def build_command(self, command, **kwargs):
    #     var_dict = defaultdict(str, kwargs)
    #     built_command = self.templates[command].format_map(var_dict)
    #     return built_command
    #
    # def generate_templates(self, command):
    #     template = self.template[command]
        # template = ""
        # command_order = config.pop('command_order')
        # for cmd in command_order:
        #     template += (cmd + " ")
        #     template += (config.pop(cmd) + " ")
        #
        # for key, value in config.items():
        #     template += (key + " " + value + " ")

        self.templates[command] = template

if __name__ == '__main__':
    template = "read_fast5_basecaller.py --input {input} --save_path {save_path} --flowcell {flowcell} --kit {kit} --output_format fastq --worker_threads 1 --reads_per_fastq 1000"
    command_kwargs = [{'input': 'this_input',
                      'save_path': 'this.save_path',
                      'flowcell': 'this.flowcell',
                      'kit': 'this.kit'},
                      {'input': 'this_input1',
                       'save_path': 'this.save_path1',
                       'flowcell': 'this.flowcell1',
                       'kit': 'this.kit1'}
                      ]
    cb = CommandBuilder(command_kwargs, template)
    cmds = cb.run()
    print(cmds)
