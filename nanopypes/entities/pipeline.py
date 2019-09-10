



class PipelineConfiguration:
    def __init__(self, pipeline_path=None, **user_input):

        pipeline_data = self._get_yaml_config(pipeline_path)
        self._pipeline_config = pipeline_data
        self._pipe_configs = {}

        self._pipeline_id = pipeline_data.pop("pipeline_id")
        self._pipeline_order = pipeline_data.pop("pipeline_order")
        self._pipeline_tools = pipeline_data.pop("pipeline_tools")
        self._get_pipe_configs()

        self.user_input = user_input or {}
        self._check_user_input()
        self._update_pipe_configs()

    @property
    def pipe_configs(self):
        return self._pipe_configs

    @property
    def pipeline_config(self):
        return self._pipeline_config

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
        for pipe, cmd in self._pipeline_tools:
            #print(pipe, cmd)
            command = self.pipe_configs[pipe]["commands"][cmd]['template'].format_map(user_input)
            self.pipe_configs[pipe]["commands"][cmd]['template'] = command
            #print("Command: ", command)

    def _get_yaml_config(self, path):
        with open(path, 'r') as config:
            data = yaml.safe_load(config)
        return data

    def _get_pipe_configs(self):
        import os

        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, "configs", "pipes.yml")
        all_pipe_configs = self._get_yaml_config(path)
        for pipe, values in self._pipeline_config["pipe_configs"].items():
            try:
                all_pipe_configs[pipe].update(values)
            except KeyError:
                all_pipe_configs[pipe] = values

        for tool, command in self._pipeline_tools:
            self._pipe_configs[tool] = all_pipe_configs[tool]
        print(self._pipe_configs)

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
            if i not in self.user_input:
                new_value = input("You forgot a Pipeline Parameter...\nPlease enter a value for {}: ".format(i))
                self.user_input[i] = new_value
        #print(self.user_input)

        #self._search_dict(self._pipe_configs)

    def _search_dict(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self._search_dict(value)
            elif isinstance(value, str):
                user_inputs = re.findall(r'{{USER_INPUT}}', value)
                if len(user_inputs) > 0:
                    raise Exception("Check your config values: ", key)
