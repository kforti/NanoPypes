import yaml
import subprocess
import json
import datetime
from pathlib import Path

from nanopypes.pipes.basecaller import AlbacoreBasecaller
from nanopypes.compute import NanopypesCluster

from write_job import HPCJob

from distributed import Client


class HPCJobComponent(HPCJob):
    def __init__(self, script_name, cores, mem, queue, walltime, commands,
                 job_name=None, shell=None, out=None, err=None, save_path=None):
        super().__init__(script_name, cores, mem, queue, walltime, commands, job_name, shell, out, err, save_path)


    def job_submission(self, script_path):
        cmd = "bsub < {script_path}".format(script_path=script_path)
        process = subprocess.run(cmd, shell=True, check=True)
        return

    def __call__(self, script_path):
        self.job_submission(script_path)


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


class ProfileRun:

    def __init__(self, name, config_path='profile_params', output_path="profile_run_data"):
        self.name = name
        self.component_configs = self.load_config(config_path)
        self.output = output_path
        self.pipe_handler = {'nanopypes_albacore': AlbacoreBasecaller,
                             'albacore_commandline': HPCJobComponent}
        self.component_handler = {}

        self.build_components()

    def load_config(self, path):
        with open(path, 'r') as config:
            config_data = yaml.safe_load(config)

        try:
            run_params = config_data["profile_runs"][self.name]
        except:
            raise IOError("Profile run name not in profile params config")
        return run_params

    def build_components(self):
        for component in self.component_configs:
            component_config = self.component_configs[component]
            if component_config["component_type"] == "pipe":
                cluster = NanopypesCluster.from_dict(component_config["compute"])
                cluster.build_cluster()

                component_config["pipe"]["cluster"] = cluster
                pipe = self.pipe_handler[component_config["component_handler"]]
                pipe = pipe.from_dict(component_config["pipe"])
                self.component_handler[component] = pipe
                #print(pipe.__dict__)

            elif component_config["component_type"] == "hpc_job":
                alb_conf = component_config["albacore"]
                job_config = component_config["job_script"]
                command = build_basecall_command(alb_conf)
                job_config["commands"] = [command]

                hpc_component = HPCJobComponent.from_dict(job_config)
                path = "job_scripts/" + job_config["script_name"]
                hpc_component.write_job_script(path)

                self.component_handler[component] = hpc_component
                #print(job_script.__dict__)


    def run(self, component=None):
        if component:
            comp = self.component_handler[component]
            self._execute_component(comp)
        else:
            for comp in self.component_handler.values():
                self._execute_component(comp)

    def _execute_component(self, comp_handle):
        comp_data = comp_handle.__dict__
        try:
            comp_data["cluster"] = comp_handle.cluster_data
        except:
            pass
        start_time = datetime.datetime.now()
        comp_handle()
        end_time = datetime.datetime.now()
        t = (str(start_time), str(end_time), str(end_time-start_time))
        comp_data["time"] = t
        comp_data["input_path"] = str(comp_data["input_path"])
        comp_data["save_path"] = str(comp_data["save_path"])
        print(comp_data)
        comp_data.pop("client")
        comp_data["cluster"].pop('_cluster')
        comp_data["cluster"].pop("clients")
        save_path = Path(self.output).joinpath("profile_runs.js")
        with open(save_path, 'a') as file:
            json.dump(comp_data, file)




if __name__ == '__main__':
    pr = ProfileRun("run1")
    pr.run()

