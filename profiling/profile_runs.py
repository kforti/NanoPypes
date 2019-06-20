import yaml
import json
import datetime
from pathlib import Path

from nanopypes.pipes.basecaller import AlbacoreBasecaller
from nanopypes.compute import ClusterManager
from nanopypes.tasks.lsf_job import LSFJob




basecall_template = "read_fast5_basecaller.py --flowcell {flowcell} --kit {kit} --output_format {output_format} --save_path {save_path} --worker_threads {worker_threads} --input {input} --reads_per_fastq_batch {reads_per_fatsq} {}"

def build_basecall_command(config, recursive=True):
    """ Method for creating the string based command for running the albacore basecaller from the commandline."""
    command = "read_fast5_basecaller.py "
    command += "--flowcell {} ".format(config["flowcell"])
    command += "--kit {} ".format(config["kit"])
    command += "--output_format {} ".format(config["output_format"])
    command += "--save_path {} ".format(config["save_path"])
    command += "--worker_threads {} ".format(config["threads"])
    command += "--input {} ".format(config["input_path"])
    command += "--reads_per_fastq_batch {} ".format(config["reads_per_fastq"])
    if recursive:
        command += "-r "
    return command


class ProfileConfig:
    def __init__(self, path):
        self._path = path
        self._load_config()

    def _load_config(self):
        with open(self._path, 'r') as config:
            self.config_data = yaml.safe_load(config)

    def __iter__(self):
        for component in self.config_data["components"]:
            yield component

    def __getitem__(self, item):
        return self.config_data["components"][item]


class ComponentRun:
    def run(self):
        pass

    def _is_jsonable(self, value):
        try:
            json.dumps(value)
            return True
        except:
            return False


class PipeComponentRun(ComponentRun):
    pipe_handler = {'nanopypes_albacore': AlbacoreBasecaller,}

    def __init__(self, pipe_dict, compute_dict, pipe_handle):
        self.cluster = ClusterManager.from_dict(compute_dict)
        self.cluster.build_cluster()

        pipe_dict["cluster"] = self.cluster
        self.pipe = self.pipe_handler[pipe_handle].from_dict(pipe_dict)

        self.start_run = None
        self.end_run = None

    def run(self):
        pipe_data = self.pipe.__dict__
        start_time = datetime.datetime.now()
        self.pipe()
        end_time = datetime.datetime.now()
        pipe_data["time"] = (str(start_time), str(end_time), str(end_time - start_time))

        try:
            pipe_data["input_path"] = str(pipe_data["input_path"])
        except:
            pass
        try:
            pipe_data["save_path"] = str(pipe_data["save_path"])
        except:
            pass

        pipe_data_copy = {}
        for key, value in pipe_data.items():
            if self._is_jsonable(value) is False:
                continue
            pipe_data_copy[key] = value

        return pipe_data_copy


class LSFComponentRun:
    def __init__(self, job_dict, command_dict):
        self.job_dict = job_dict
        self.command_dict = command_dict
        self.command = build_basecall_command(self.command_dict)
        self.job_dict["commands"] = [self.command]

        self.job = LSFJob.from_dict(self.job_dict)
        self.job.write_job_script()

    def run(self):
        job_data = self.job.__dict__
        start_time = datetime.datetime.now()
        self.job.run()
        end_time = datetime.datetime.now()
        job_data["time"] = (str(start_time), str(end_time), str(end_time - start_time))
        job_data.update(self.command_dict)
        for key, value in job_data.items():
            if self._is_jsonable(value) is False:
                job_data.pop(key)
        return job_data


class ProfileRun:

    def __init__(self, name, config_path='profile_params', output_path="profile_run_data"):
        self.name = name
        self.component_configs = self.load_config(config_path)
        self.output = output_path

        self.component_handler = {}

        self.build_components()

    def load_config(self, path):
        with open(path, 'r') as config:
            config_data = yaml.safe_load(config)

        try:
            run_params = config_data[self.name]
        except:
            raise IOError("Profile run name not in profile params config")
        return run_params

    def build_components(self):
        for component in self.component_configs:
            component_config = self.component_configs[component]

            if component_config["component_type"] == "pipe":
                id = component_config["component_id"]
                self.component_handler[id] = PipeComponentRun(pipe_dict=component_config["pipe"],
                                                              compute_dict=component_config["compute"],
                                                              pipe_handle=component_config["pipe_handler"])

            elif component_config["component_type"] == "hpc_job":
                command = component_config["command"]
                job_config = component_config["job_script"]
                id = component_config["component_id"]

                self.component_handler[id] = LSFComponentRun(job_dict=job_config,
                                                             command_dict=command)

    def run(self, component=None):
        if component:
            comp = self.component_handler[component]
            print("executing comp...", comp.__dict__)
            self._execute_component(comp)
        else:
            for comp in self.component_handler.values():
                print("executing comp...", comp.__dict__)
                self._execute_component(comp)

    def _execute_component(self, comp_handle):
        profile_data = comp_handle.run()
        save_path = Path(self.output).joinpath("profile_runs.js")

        with open(str(save_path), 'a') as file:
            json.dump(profile_data, file)



if __name__ == '__main__':
    config = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/profiling/test_profile_params"
    pr = ProfileRun(name="run1", config_path=config)
    pr.run()

    # (cluster_type='lsf',
    # job_time='01:00',
    # project='/ project / umw_athma_pai',
    # queue='short',
    # workers_per_job=5,
    # num_workers=5,
    # worker_cores=1,
    # worker_memory=2048,
    # debug=True)

