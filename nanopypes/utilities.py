from functools import wraps
from collections import defaultdict
import yaml
import re



class CommandBuilder:
    """
    Class for generating command line command strings from a template. Templates are used to generate
    the command across partitioned data (for parallel processing).

    Args:
        - template (string): a string template with variables wrapped in brackets {}.
            (Example template: 'minimap2 -ax map-ont {ref} {read} -o {output}')
    """
    def __init__(self, commands, template_config):
        self.commands = commands
        self.template_config = template_config

        self.templates = {}
        for command in self.commands:
            self.generate_templates(command)


    def build_command(self, command, **kwargs):
        var_dict = defaultdict(str, kwargs)
        built_command = self.templates[command].format_map(var_dict)
        return built_command

    def generate_templates(self, command):
        template = self.template_config[command]
        # template = ""
        # command_order = config.pop('command_order')
        # for cmd in command_order:
        #     template += (cmd + " ")
        #     template += (config.pop(cmd) + " ")
        #
        # for key, value in config.items():
        #     template += (key + " " + value + " ")

        self.templates[command] = template


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class Configuration:
    def __init__(self, pipeline_path, user_input):
        self.pipeline_config = self._get_yaml_config(pipeline_path)
        self._pipe_configs = {}
        self._pipeline_id = self.pipeline_config.pop("pipeline_id")
        self._pipeline_order = self.pipeline_config.pop("pipeline_order")
        self._get_pipe_configs()

        self._compute_config_path = self.pipeline_config.pop("compute_config_path")
        self._compute_id = self.pipeline_config.pop("compute_id")
        compute_config = self._get_yaml_config(self._compute_config_path)
        self._compute_config = compute_config.pop(self._compute_id)

        self.user_input = user_input
        self._check_user_input()
        self._update_pipe_configs()
        print(self._pipe_configs)

    @property
    def compute_config(self):
        return self._compute_config

    @property
    def pipe_configs(self):
        return self._pipe_configs

    @property
    def pipeline_order(self):
        return self._pipeline_order

    @property
    def input_path(self):
        return self.pipeline_config["input_path"]

    @property
    def save_path(self):
        return self.pipeline_config["save_path"]

    def _update_pipe_configs(self):
        user_input = SafeDict(self.user_input)
        for pipe, cmd in self._pipeline_order:
            print(pipe, cmd)
            command = self.pipe_configs[pipe]["commands"][cmd].format_map(user_input)
            print("Command: ", command)

    def _get_yaml_config(self, path):
        with open(path, 'r') as config:
            data = yaml.safe_load(config)
        return data

    def _get_pipe_configs(self):
        import os

        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, "configs", "pipes.yml")
        all_pipe_configs = self._get_yaml_config(path)
        for pipe, values in self.pipeline_config["pipe_configs"].items():
            try:
                all_pipe_configs[pipe].update(values)
            except KeyError:
                all_pipe_configs[pipe] = values

        for pipe, command in self._pipeline_order:
            self._pipe_configs[pipe] = all_pipe_configs[pipe]

        return self._pipe_configs

    def _check_user_input(self):
        expected_user_input = []
        for pipe, data in self._pipe_configs.items():
            try:
                user_input = data["user_input"]
                expected_user_input.extend(user_input)
            except KeyError:
                pass
        for i in expected_user_input:
            try:
                print(i, self.user_input[i])
            except KeyError:
                new_value = input("You forgot a Pipeline Parameter...\nPlease enter a vlue for {}: ".format(i))
                self.user_input[i] = new_value
        print(self.user_input)

        #self._search_dict(self._pipe_configs)


    def _search_dict(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self._search_dict(value)
            elif isinstance(value, str):
                user_inputs = re.findall(r'{{USER_INPUT}}', value)
                if len(user_inputs) > 0:
                    raise Exception("Check your config values: ", key)



#####################
# Exceptions
#####################

class SubprocessError(Exception):
    pass

class InValidTaskError(KeyError):
    pass


if __name__ == '__main__':
    import os
    import sys

    path = os.path.dirname(sys.modules['__main__'].__file__)
    print(path)
    # path = "configs/pipeline.yml"
    # config = Configuration(path)
    # print(config.compute_config)
    # print(config.pipe_configs)
    # print(config.pipeline_order)

