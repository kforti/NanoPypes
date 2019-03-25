from datetime import datetime
from yaml import load
import logging


# logging.basicConfig(filename='tests/logging/commandline.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Configuration:
    def __init__(self, config):
        extension = config.split('.')[1]
        if extension == "yml":
            with open(config, "r") as file:
                settings = load(file)
        else:
            raise IOError("Incorrect configuration file type")
        try:
            self._networking = settings["networking"]
            self._basecall = settings["basecall"]
            self._compute = settings["compute"]
            self._pipes = settings["pipe"]
        except Exception as e:
            print("exception raised")
            print(e)

    @property
    def networking(self):
        return [NetworkingConfig(network) for network in self._networking.keys()]

    @property
    def basecall(self):
        return BasecallConfig(self._basecall)

    @property
    def compute(self):
        compute = [ComputeConfig(self._compute[compute]) for compute in self._compute.keys()]
        return compute

    @property
    def pipe(self):
        if len(self._pipes.keys()) > 1:
            pipe = [PipesConfig(self._pipes[pipe]) for pipe in self._pipes.keys()]
        elif len(self._pipes.keys()) == 1:
            pipe = PipesConfig(self._pipes)
        return pipe

class BasecallConfig:
    default_settings = {"kit": None,
                        "flowcell": None,
                        "save_path": None,
                        "input_path": None,
                        "barcoding": None,
                        "output_format": None,
                        "worker_threads": None,
                        "recursive": None,
                        "reads_per_fastq": None
                        }
    def __init__(self, settings):
        if settings:
            self._settings = settings
        elif settings == None:
            self._settings = self.default_settings

        # self._basecaller = self._settings["basecaller"]
        self._kit = self._settings["kit"]
        self._flowcell = self._settings["flowcell"]
        self._save_path = self._settings["save_path"]
        self._input_path = self._settings["input_path"]
        self._barcoding = self._settings["barcoding"]
        self._output_format = self._settings["output_format"]
        self._worker_threads = self._settings["worker_threads"]
        self._recursive = self._settings["recursive"]
        self._reads_per_fastq = self._settings["reads_per_fastq"]

    def kit(self, name=None):
        if name:
            self._kit = name
        return self._kit

    def flowcell(self, name=None):
        if name:
            self._flowcell = name
        return self._flowcell

    def save_path(self, path=None):
        if path:
            self._save_path = path
        return self._save_path

    def input_path(self, path=None):
        if path:
            self._input_path = path
        return self._input_path

    def barcoding(self, bool=False):
        if bool:
            self._barcoding = bool
        return self._barcoding

    def output_format(self, format=None):
        if format:
            self._output_format = format
        return self._output_format

    def worker_threads(self, workers=None):
        if workers:
            self._worker_threads = workers
        return self._worker_threads

    def recursive(self, bool='none'):
        if bool != 'none':
            self._recursive = bool
        return self._recursive

    def reads_per_fastq(self, num=None):
        if num:
            self._reads_per_fastq = num
        return self._reads_per_fastq


class NetworkingConfig:
    def __init__(self, settings):
        self._settings = settings


class ComputeConfig:
    default_settings = {"ncpus": None,
                        "job_time": None,
                        "mem": None,
                        "project": None,
                        "queue": None,
                        "workers": None,
                        "scale_value": None,
                        "cores": None,
                        "memory": None,
                        "cluster_type": "local",
                        }

    def __init__(self, settings):
        if settings:
            self._settings = settings
        elif settings == None:
            self._settings = self.default_settings

        self._ncpus = self._settings["ncpus"]
        self._job_time = self._settings["job_time"]
        self._mem = self._settings["mem"]
        self._project = self._settings["project"]
        self._queue = self._settings["queue"]
        self._workers =self._settings["workers"]
        self._scale_value = self._settings["scale_value"]
        self._cores = self._settings["cores"]
        self._memory = self._settings["memory"]
        self._cluster_type = self._settings["cluster_type"]

    def ncpus(self, num=None):
        if num:
            self._ncpus = num
        return self._ncpus

    def job_time(self, time=None):
        if time:
            self._job_time = time
        return self._job_time

    def mem(self, value=None):
        if value:
            self._mem = value
        return self._mem

    def project(self, path=None):
        if path:
            self._project = path
        return self._project

    def queue(self, name=None):
        if name:
            self._queue = name
        return self._queue

    def workers(self, num=None):
        if num:
            self._workers = num
        return self._workers

    def scale_value(self, value=None):
        if value:
            self._scale_value = value
        return self._scale_value

    def cores(self, num=None):
        if num:
            self._cores = num
        return self._cores

    def memory(self, value=None):
        if value:
            self._memory = value
        return self._memory

    def cluster_type(self, name=None):
        if name:
            self._cluster_type = name
        return self._cluster_type


class PipesConfig:
    def __init__(self, settings):
        self._settings = settings
        self._name = self._settings["name"]

    @property
    def name(self):
        return self._name



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
        if config == None:
            return {}
        extension = config.split('.')[1]
        if extension == "yml":
            file = open(config, "r")
            return load(file)
