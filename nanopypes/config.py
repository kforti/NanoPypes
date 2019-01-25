


class Config:
    def __init__(self, config):
        self._config = self.parse_config(config)

    @property
    def config(self):
        return self._config

    @property
    def basecall_config(self):
        return self._config["basecall_config"]

    def parse_config(self, config):
        extension = config.split('.')[1]
        if extension == "yml":
            file = open(config, "r")
            return load(file)

class BasecallConfig(Config):

    def __init__(self, config, **kwargs):
        print("setting configuration...")
        super().__init__(config)
        self.bc_config = super().basecall_config
        self._parse_kwargs(**kwargs)

        logger.info("Basecall command initiated at %s with settings: %s" % (datetime.now(), self.bc_config))

    def _parse_kwargs(self, **kwargs):
        """parse the kwargs passed into the config and update
        the config settings based on the arguments passed"""
        for key, value in kwargs.items():
            if value != None and key != "config":
                self.bc_config[key] = value
            else:
                continue

    @property
    def kit(self):
        return self.bc_config["kit"]

    @property
    def flowcell(self):
        return self.bc_config["flowcell"]

    @property
    def save_path(self):
        return self.bc_config["save_path"]

    @property
    def input_path(self):
        return self.bc_config["input_path"]

    @property
    def barcoding(self):
        return self.bc_config["barcoding"]

    @property
    def output_format(self):
        return self.bc_config["output_format"]

    @property
    def worker_threads(self):
        return self.bc_config["worker_threads"]

    @property
    def recursive(self):
        return self.bc_config["recursive"]

    #######################################################################
    ## Cluster properties
    #######################################################################

    @property
    def ncpus(self):
        return self.bc_config["cluster"]["ncpus"]

    @property
    def job_time(self):
        return self.bc_config["cluster"]["job_time"]

    @property
    def mem(self):
        return self.bc_config["cluster"]["mem"]

    @property
    def project(self):
        return self.bc_config["cluster"]["project"]

    @property
    def queue(self):
        return self.bc_config["cluster"]["queue"]

    @property
    def workers(self):
        return self.bc_config["cluster"]["workers"]

    @property
    def cores(self):
        return self.bc_config["cluster"]["cores"]

    @property
    def memory(self):
        return self.bc_config["cluster"]["memory"]
