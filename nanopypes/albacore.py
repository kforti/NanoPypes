import os
import dask
import subprocess
import logging
import shutil
from pathlib import Path
from dask_jobqueue import LSFCluster
from dask.distributed import Client, wait
from .data_types import RawData
from .utils import temp_dirs, remove_temps, dir_generator, copyfiles

class Albacore:
    """ Conatains the data associated with making the command to run the basecaller.
    Build the command with build_command()
   """
    def __init__(self, input, flowcell, kit, save_path, output_format,
                 barcoding=None,
                 reads_per_fastq=1000):
        self.flow_cell = flowcell
        self.kit = kit
        self.save_path = save_path
        self.barcoding = barcoding
        self.output_format = output_format
        self.config_set = False
        if reads_per_fastq:
            self.reads_per_fastq = reads_per_fastq

        if type(input).__name__ == 'RawData':
            self.input = input

        elif type(input).__name__ == 'str':
            #convert input string to a Fast5Dir
            self.input = RawData(input)
        else:
            raise AttributeError("The wrong input data format is being passed to Albacore."
                                 " Make sure you are providing a string representing a valid path to your data.")

        self.next_dir = dir_generator(self.input.path)

    @property
    def basecall_input(self):
        """ Retrive the name of the input directory and the list of commands associated with that directory as a dict {dir_name: [List of commands}"""
        dir = next(self.next_dir)
        tmp_dirs = temp_dirs(dir, self.input.path)
        commands_list = []

        # Make sure the save-path is created
        save_path = Path(self.save_path).joinpath(dir)
        if not save_path.exists():
            save_path.mkdir()

        for i in tmp_dirs:
            command = self.build_command(i, str(save_path))
            commands_list.append(command)
        commands_tupl = (dir, commands_list)
        return commands_tupl

    @property
    def num_dirs(self):
        num_dirs = self.input.num_dirs
        return num_dirs

    def remove_temps(self):
        remove_temps(self.input.path)

    def build_command(self, input_dir, save_dir):
        """ Method for creating the string based command for running the albacore basecaller from the commandline."""
        command = "read_fast5_basecaller.py "
        command += "--flowcell " + self.flow_cell + " "
        command += "--kit " + self.kit + " "
        command += "--output_format " + self.output_format + " "
        command += "--save_path " + save_dir + " "
        command += "--worker_threads 1 "
        command += "--input " + input_dir + " "

        if self.barcoding:
            command += "--barcoding "

        if self.output_format == "fastq":
            command += "--reads_per_fastq " + str(self.reads_per_fastq) + " "

        return command

    def collapse_save(self, save_path=None):
        """ Collapse all the data into the expected output"""
        if save_path == None:
            save_path = self.save_path
        # List of data directories generated from the parallel basecalling
        data_dirs = os.listdir(save_path)

        # Create the expected directories in the save_path
        # calibration_strand, pass and fail directories within the workspace directory
        workspace = "/".join([save_path, "workspace"])
        os.mkdir(workspace)
        calibration = "/".join([workspace, "calibration_strands"])
        os.mkdir(calibration)
        pss = "/".join([workspace, "pass"])
        os.mkdir(pss)
        fail = "/".join([workspace, "fail"])
        os.mkdir(fail)

        # directories for the other files produced by the basecaller script (main files)
        config_file = "/".join([save_path, "configuration.cfg"])
        pipe_file = "/".join([save_path, "pipeline.log"])
        seqsum_file = "/".join([save_path, "sequencing_summary.txt"])
        seqtel_file = "/".join([save_path, "sequencing_telemetry.js"])

        # Iterate through the data directories in the save_path
        for dir in data_dirs:
            dir_path = "/".join([save_path, dir])

            # The dir's sequence summary file- add contents to the main sequence summary file
            dir_seqsum_file = "/".join([dir_path, "sequencing_summary.txt"])
            with open(dir_seqsum_file, "r") as inp:
                with open(seqsum_file, "a") as out:
                    for line in inp:
                        out.write(line)

            # the dir's config file- move one config file to the main config file location
            dir_config_file = "/".join([dir_path, "configuration.cfg"])
            if not self.config_set:
                shutil.copyfile(dir_config_file, config_file)
                self.config_set = True

            # The dir's sequence_telemetry.js file-
            dir_seqtel_file = "/".join([dir_path, "sequencing_telemetry.js"])
            with open(dir_seqtel_file, "r") as inp:
                with open(seqtel_file, "a") as out:
                    for line in inp:
                        out.write(line)

            dir_pipe_file = "/".join([dir_path, "pipeline.log"])
            with open(dir_pipe_file, "r") as inp:
                with open(pipe_file, "a") as out:
                    for line in inp:
                        out.write(line)

            # Set the directories in the dir
            cal_data = "/".join([dir_path, "workspace", "calibration_strands", "0"])
            pss_data = "/".join([dir_path, "workspace", "pass", "0"])
            fail_data = "/".join([dir_path, "workspace", "fail", "0"])

            # calibration_strands in save_dir
            cal_save = "/".join([calibration, dir])
            os.mkdir(cal_save)
            copyfiles(cal_data, cal_save)

            # pass in save_dir
            pss_save = "/".join([pss, dir])
            os.mkdir(pss_save)
            copyfiles(pss_data, pss_save)

            # fail in save_dir
            fail_save = "/".join([fail, dir])
            os.mkdir(fail_save)
            copyfiles(fail_data, fail_save)

            shutil.rmtree(dir_path)

class Basecaller:
    """ Cluster based task manager for running the basecaller in parallel"""
    def __init__(self, albacore, queue, project, job_time, initial_workers, cores, memory, cluster_type="LSF"):
        self.albacore = albacore
        self.workers = initial_workers
        self.queue = queue
        self.project = project
        self.walltime = job_time
        self.cores = cores
        self.memory = memory
        self.cluster_type = cluster_type
        self._data_dirs = None
        logging.basicConfig(filename='logging/basecall.log', level=logging.DEBUG)

    def parallel_basecaller(self, test=False):
        try:
            self._connect_cluster()
            num_dirs = self.albacore.num_dirs
            logging.info('Number of Directories: ' + str(num_dirs))
            try:
                for i in range(num_dirs):
                    commands = self.albacore.basecall_input
                    func = self._build_func()
                    if test:
                        logging.info('This run is a test')
                        logging.info(str(commands[0: self.workers]))
                        basecalled_reads = self.client.map(func, commands[1])
                        break
                    else:
                        logging.info('This run is not a test')
                        basecalled_reads = self.client.map(func, commands[1])
                    wait(basecalled_reads)
                    self.albacore.remove_temps()

            except StopIteration:
                return

            self.albacore.collapse_save()

        except Exception as e:
            logging.info("Exception raised during the basecalling: " + str(e))
            self.cluster.kill_all_jobs()

    def _connect_cluster(self):
        """Connects to cluster and sets client"""
        if self.cluster_type == "LSF":
            logging.info("connecting to cluster")
            self.cluster = LSFCluster(queue=self.queue,
                                 project=self.project,
                                 walltime=self.walltime,
                                 # ncpus=self.ncpus,
                                 # mem=self.mem,
                                 cores=self.cores,
                                 memory=self.memory)

        else:
            logging.info("Did not connect to cluster")

        # Scale the number of dask workers across multiple cluster jobs -> the value passed to cluster.scale() is the number of jobs
        logging.info("scaling to " + str(self.workers) + " workers")
        self.cluster.scale(self.workers)
        self.client = Client(self.cluster)
        logging.info("client status: " + self.client.status)

    def _build_func(self):
        def func(command):
            process = subprocess.Popen([command], shell=True)
            process.wait()

        return func


def create_file(name):
    with open(name, "w") as f:
        f.write("some data")

print("hi")

# data_names = ["calibration_strands", "fail", "pass"]
# file_names = ["sequencing_telemetry.js", "pipeline.log", "configuration.cfg", "sequencing_summary.txt"]
#
# save_data = Path("./save_data")
# for i in range(10):
#     name = str(i)
#     dir_path = save_data.joinpath(name)
#     os.mkdir(dir_path)
#     for file in file_names:
#         n = dir_path.joinpath(file)
#         create_file(n)
#     workspace = dir_path.joinpath("workspace")
#     workspace.mkdir()
#     for y in data_names:
#         p = workspace.joinpath(y)
#         p.mkdir()
#         c = p.joinpath("0")
#         c.mkdir()
#         for f in range(4):
#             f_name = str(f)
#             fp = c.joinpath(f_name)
#             with open(fp, "w") as f:
#                 f.write("here is some data...")
