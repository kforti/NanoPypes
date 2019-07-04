import yaml

class NanoPypesRunner:

    def __init__(self, pipes_configs=['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/nanopypes/configs/pipes.yml']):
        self._pipe_configs = self.load_config(pipes_configs)

        self.component_handler = {}

    def load_config(self, paths):
        config_data = {}
        for path in paths:
            with open(path, 'r') as config:
                config_data.update(yaml.safe_load(config))

        return config_data

    def get_pipe(self, pipe):
        return self._pipe_configs[pipe]

def gen_command(config_dict):
    full_command = ""
    command_order = config_dict.pop('command_order')
    for command in command_order:
        full_command += (command + " ")
        full_command += (config_dict.pop(command) + " ")

    for key, value in config_dict.items():
        full_command += (key + " " + value + " ")

    return full_command


if __name__ == '__main__':
    npr = NanoPypesRunner()
    albacore_config = npr.get_pipe('albacore')
    cmd = gen_command(albacore_config['command'])
    print(cmd)


