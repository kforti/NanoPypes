import os
import dask
import subprocess
import logging
import time
from pathlib import Path
from dask_jobqueue import LSFCluster
from dask.distributed import Client, progress, as_completed
from nanopypes.utils import temp_dirs
from nanopypes.objects.raw import Sample
from nanopypes.config import BasecallConfig

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class Albacore:
    """ Conatains the data associated with making the command to run the basecaller.
    Build the command with build_command()
   """
    def __init__(self, input,
                 flowcell=None,
                 kit=None,
                 save_path=None,
                 output_format=None,
                 reads_per_fastq=None,
                 barcoding=None,):

        if isinstance(input, Sample):
            self.input = input
            self.flow_cell = flowcell
            self.kit = kit
            self._save_path = save_path
            self.barcoding = barcoding
            self.output_format = output_format
            if reads_per_fastq:
                self.reads_per_fastq = reads_per_fastq

        elif input.split('.')[1] == "yml":
            config = BasecallConfig(input, flowcell=flowcell,
                                    kit=kit,
                                    save_path=save_path,
                                    output_format=output_format,
                                    barcoding=barcoding,
                                    reads_per_fastq=reads_per_fastq)
            self.input = Sample(config.input_path)
            self.flow_cell = config.flowcell
            self.kit = config.kit
            self._save_path = config.save_path
            self.barcoding = config.barcoding
            self.output_format = config.output_format
            if reads_per_fastq:
                self.reads_per_fastq = config.reads_per_fastq

        if self.output_format == "fastq" and reads_per_fastq == None:
            self.reads_per_fastq = 1000

    @property
    def input_path(self):
        return self.input.path

    @property
    def save_path(self):
        return self._save_path

    @property
    def basecall_input(self):
        """ Retrive the name of the input directory and the list of commands
         associated with that directory as a dict {dir_name: [List of commands}"""
        next_bin = next(self.batch_generator)
        bin_path = Path(self.input_path).joinpath(next_bin)
        tmp_dirs = temp_dirs(bin_path, self.input.path)
        commands_list = []

        # Make sure the save-path is created
        save_path = Path(self._save_path).joinpath(next_bin)
        if not save_path.exists():
            save_path.mkdir()

        for i in tmp_dirs:
            command = self.build_command(i, str(save_path))
            commands_list.append(command)
        commands_tupl = (next_bin, commands_list)
        return commands_tupl

    @property
    def batches(self):
        batches = [Path(self.input_path).joinpath(i) for i in os.listdir(str(self.input_path))]
        return batches

    @property
    def num_batches(self):
        return self.input.num_batches

    @property
    def batch_generator(self):
        for bin in self.batches:
            yield bin

    def build_command(self, input_dir, batch_number):
        """ Method for creating the string based command for running the albacore basecaller from the commandline."""
        temp_dir_num = input_dir.split('/')[-1]
        command = ["read_fast5_basecaller.py",]
        command.extend(["--flowcell", self.flow_cell])
        command.extend(["--kit", self.kit])
        command.extend(["--output_format", self.output_format])
        command.extend(["--save_path", self._save_path + "/" + batch_number + "/" + temp_dir_num])
        command.extend(["--worker_threads", "1"])
        command.extend(["--input",  input_dir])
        if self.barcoding:
            command.append("--barcoding")
        if self.output_format == "fastq":
            command.extend(["--reads_per_fastq", str(self.reads_per_fastq)])
        return command

    @classmethod
    def build_func(self):
        def func(command):
            process = subprocess.check_output(command)
            return process
        return func

class Cluster:
    """ Cluster based task manager for running the basecaller in parallel"""
    def __init__(self, config=None, queue=None, project=None, job_time=None, cores=None, mem=None,
                 ncpus=None, memory=None, workers=None, scale_value=None, cluster_type=None, time_out=2000):

        self.config = BasecallConfig(config, queue=queue, project=project, job_time=job_time, cores=cores,
                                     memory=memory, workers=workers, cluster_type=cluster_type,
                                     scale_value=scale_value, mem=mem, ncpus=ncpus)
        self.queue = self.config.queue
        self.project = self.config.project
        self.walltime = self.config.job_time
        self.cores = self.config.cores
        self.memory = self.config.memory
        self.mem = self.config.mem
        self.ncpus = self.config.ncpus
        self.cluster_type = self.config.cluster_type
        self.workers = self.config.workers
        self.scale_value = self.config.scale_value
        self.time_out = time_out

    @property
    def settings(self):
        return self.__dict__

    @property
    def expected_workers(self):
        return self.workers

    @expected_workers.setter
    def expected_workers(self, value):
        self.workers = value

    @property
    def connected_workers(self):
        return len(self.cluster.scheduler.workers)

    @property
    def pending_jobs(self):
        return self.cluster.pending_jobs

    @property
    def running_jobs(self):
        return self.cluster.running_jobs

    @property
    def finished_jobs(self):
        return self.cluster.finished_jobs

    def scale(self, value):
        """Add workers to cluster connection"""
        self.cluster.scale(value)
        timer = 0
        while len(self.cluster.scheduler.workers) < value:
            time.sleep(1)
            print("Client: ", self.client)
            print("workers: ", len(self.cluster.scheduler.workers))
            print("expected workers: ", value)
            print("pending jobs: ", self.cluster.pending_jobs)
            print("jobs: ", len(self.cluster.running_jobs))
            timer += 1
            if timer > self.time_out:
                raise ConnectionError("Could not start all workers before time_out")

        self.workers = value

    def map(self, func, iterable):
        self.futures = self.client.map(func, iterable)
        return self.futures

    def show_progress(self):
        progress(self.futures)

    def connect(self):
        """ Establish connection to cluster"""
        assert self.workers != None, "You must assign number of workers"
        assert self.queue != None, "You must assign a queue to run your workers on"

        if self.cluster_type == "LSF":
            logging.info("connecting to cluster")
            self.cluster = LSFCluster(queue=self.queue, #Passed to #BSUB -q option.
                                      project=self.project, #Passed to #BSUB -P option.
                                      processes=self.workers,
                                      walltime=self.walltime, #Passed to #BSUB -W option.
                                      ncpus=self.ncpus, #Passed to #BSUB -n option.
                                      mem=self.mem, #Passed to #BSUB -M option.
                                      cores=self.cores,
                                      memory=self.memory,
                                      death_timeout=self.time_out)
        print("job script: ", self.cluster.job_script())
        self.client = Client(self.cluster)
        print("scale_value: ", self.scale_value)
        self.scale(self.scale_value)

        timer = 0
        # while len(self.cluster.scheduler.workers) < self.workers:
        #     time.sleep(1)
        #     #print("workers: ", self.cluster.scheduler.workers)
        #     #print("expected workers: ", self.workers)
        #     #print("pending jobs: ", self.cluster.pending_jobs)
        #     #print("jobs: ", self.cluster.running_jobs)
        #     timer += 1
        #     if timer > self.time_out:
        #         raise ConnectionError("Could not start all workers before time_out")

    def stop_jobs(self, jobs="all"):
        if jobs == "all":
            self.cluster.stop_all_jobs()
        else:
            self.cluster.stop_jobs(jobs)
