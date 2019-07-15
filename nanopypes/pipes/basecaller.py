from pathlib import Path
import os
import shutil
import datetime
import re
import subprocess


from distributed import as_completed, Client


from nanopypes.pipes.base import Pipe



def batch_generator(batches):
    for batch in batches:
        yield batch


def b_gen(input_path):
    batch_pattern = r'(^)[0-9]+($)'
    alt_batch_pattern = r'(^)batch_[0-9]+($)'
    batches = [Path(input_path).joinpath(i) for i in os.listdir(str(input_path)) if
               re.match(batch_pattern, str(i)) or re.match(alt_batch_pattern, str(i))]
    return batches


class AlbacoreBasecaller(Pipe):

    def __init__(self, cluster, input_path,
                 flowcell, kit, save_path, output_format='fastq',
                 reads_per_fastq=1000):
        print("Starting the parallel Albacore Basecaller...\n", datetime.datetime.now())
        self.input_path = Path(input_path)
        self.flowcell = flowcell
        self.kit = kit
        self.save_path = Path(save_path)
        if self.save_path.exists() == False:
            self.save_path.mkdir()
        self.output_format = output_format
        self.reads_per_fastq = reads_per_fastq
        self.num_batches = len(os.listdir(str(self.input_path)))

        self.cluster = cluster

        self.futures = []

    @classmethod
    def from_dict(cls, config_dict):
        config_dict["input_path"] = Path(config_dict["input_path"])
        save_path = config_dict["save_path"] = Path(config_dict["save_path"])
        config_dict["futures"] = []
        instance = cls.__new__(cls)
        instance.__dict__.update(config_dict)
        if save_path.exists() is False:
            save_path.mkdir()
        return instance

    @property
    def cluster_data(self):
        return self.cluster.__dict__

    def execute(self):
        num_workers = self.cluster.expected_workers
        batch_counter = 0
        batches = self.batches()
        client = self.cluster.start_cluster()

        for i in range(num_workers):
            try:
                batch = next(batches)
                print("Processing Batch...", batch)
            except StopIteration:
                break

            b_save_path = self.save_path.joinpath(batch)
            command = self.build_basecall_command(batch=batch)
            fn = self.command_function()
            bc = client.submit(fn, command)
            self.futures.append(bc)

            batch_counter += 1
            if batch_counter == num_workers:
                break

        completed = as_completed(self.futures)
        for comp in completed:
            try:
                batch = next(batches)
                print("Processing Batch...", batch)
                b_save_path = self.save_path.joinpath(batch)
                command = self.build_basecall_command(batch=batch)
                fn = self.command_function()
                new_future = client.submit(fn, command)
                completed.add(new_future)
            except StopIteration:
                pass
            #completed_batch_path = comp.result()
        client.gather(self.futures)
        collapse_data(self.save_path)

    def build_basecall_command(self, batch):
        """ Method for creating the string based command for running the albacore basecaller from the commandline."""
        input_dir = self.input_path.joinpath(batch)
        command = ["read_fast5_basecaller.py",]
        command.extend(["--flowcell", self.flowcell])
        command.extend(["--kit", self.kit])
        command.extend(["--output_format", self.output_format])
        command.extend(["--save_path", str(self.save_path.joinpath(batch))])
        command.extend(["--worker_threads", "1"])
        command.extend(["--input", str(input_dir)])

        if self.output_format == "fastq":
            command.extend(["--reads_per_fastq_batch", str(self.reads_per_fastq)])
        return command

    def batches(self):
        """Batch generator"""
        for batch in os.listdir(str(self.input_path)):
            yield batch

    def command_function(self, stdout=None):
        def func(command):
            process = subprocess.run(command, check=True)
            return process
        return func


class GuppyBasecaller(Pipe):
    """
        With config file:
          guppy_basecaller -i <input path> -s <save path> -c <config file> [options]
        With flowcell and kit name:
          guppy_basecaller -i <input path> -s <save path> --flowcell <flowcell name>
            --kit <kit name>
        List supported flowcells and kits:
          guppy_basecaller --print_workflows
        Use server for basecalling:
          guppy_basecaller -i <input path> -s <save path> -c <config file>
            --port <server address> [options]

        Command line parameters:
          --print_workflows                 Output available workflows.
          --flowcell arg                    Flowcell to find a configuration for
          --kit arg                         Kit to find a configuration for
          -m [ --model_file ] arg           Path to JSON model file.
          --chunk_size arg                  Stride intervals per chunk.
          --chunks_per_runner arg           Maximum chunks per runner.
          --chunks_per_caller arg           Soft limit on number of chunks in each
                                            caller's queue. New reads will not be
                                            queued while this is exceeded.
          --overlap arg                     Overlap between chunks (in stride
                                            intervals).
          --gpu_runners_per_device arg      Number of runners per GPU device.
          --cpu_threads_per_caller arg      Number of CPU worker threads per
                                            basecaller.
          --num_callers arg                 Number of parallel basecallers to create.
          --stay_penalty arg                Scaling factor to apply to stay probability
                                            calculation during transducer decode.
          --qscore_offset arg               Qscore calibration offset.
          --qscore_scale arg                Qscore calibration scale factor.
          --temp_weight arg                 Temperature adjustment for weight matrix in
                                            softmax layer of RNN.
          --temp_bias arg                   Temperature adjustment for bias vector in
                                            softmax layer of RNN.
          --hp_correct arg                  Whether to use homopolymer correction
                                            during decoding.
          --builtin_scripts arg             Whether to use GPU kernels that were
                                            included at compile-time.
          -x [ --device ] arg               Specify basecalling device: 'auto', or
                                            'cuda:<device_id>'.
          -k [ --kernel_path ] arg          Path to GPU kernel files location (only
                                            needed if builtin_scripts is false).
          -z [ --quiet ]                    Quiet mode. Nothing will be output to
                                            STDOUT if this option is set.
          --trace_categories_logs arg       Enable trace logs - list of strings with
                                            the desired names.
          --verbose_logs                    Enable verbose logs.
          --qscore_filtering                Enable filtering of reads into PASS/FAIL
                                            folders based on min qscore.
          --min_qscore arg                  Minimum acceptable qscore for a read to be
                                            filtered into the PASS folder
          --disable_pings                   Disable the transmission of telemetry
                                            pings.
          --ping_url arg                    URL to send pings to
          --ping_segment_duration arg       Duration in minutes of each ping segment.
          --calib_detect                    Enable calibration strand detection and
                                            filtering.
          --calib_reference arg             Reference FASTA file containing calibration
                                            strand.
          --calib_min_sequence_length arg   Minimum sequence length for reads to be
                                            considered candidate calibration strands.
          --calib_max_sequence_length arg   Maximum sequence length for reads to be
                                            considered candidate calibration strands.
          --calib_min_coverage arg          Minimum reference coverage to pass
                                            calibration strand detection.
          -q [ --records_per_fastq ] arg    Maximum number of records per fastq file, 0
                                            means use a single file (per worker, per
                                            run id).
          --enable_trimming arg             Enable adapter trimming.
          --trim_threshold arg              Threshold above which data will be trimmed
                                            (in standard deviations of current level
                                            distribution).
          --trim_min_events arg             Adapter trimmer minimum stride intervals
                                            after stall that must be seen.
          --max_search_len arg              Maximum number of samples to search through
                                            for the stall
          --reverse_sequence arg            Reverse the called sequence (for RNA
                                            sequencing).
          --u_substitution arg              Substitute 'U' for 'T' in the called
                                            sequence (for RNA sequencing).
          -i [ --input_path ] arg           Path to input fast5 files.
          -s [ --save_path ] arg            Path to save fastq files.
          -l [ --read_id_list ] arg         File containing list of read ids to filter
                                            to
          -p [ --port ] arg                 Hostname and port for connecting to
                                            basecall service (ie 'myserver:5555'), or
                                            port only (ie '5555'), in which case
                                            localhost is assumed.
          -r [ --recursive ]                Search for input files recursively.
          --fast5_out                       Choice of whether to do fast5 output.
          --override_scaling                Manually provide scaling parameters rather
                                            than estimating them from each read.
          --scaling_med arg                 Median current value to use for manual
                                            scaling.
          --scaling_mad arg                 Median absolute deviation to use for manual
                                            scaling.
          --trim_strategy arg               Trimming strategy to apply ('dna' or 'rna')
          --dmean_win_size arg              Window size for coarse stall event
                                            detection
          --dmean_threshold arg             Threhold for coarse stall event detection
          --jump_threshold arg              Threshold level for rna stall detection
          --disable_events                  Disable the transmission of event tables
                                            when receiving reads back from the basecall
                                            server.
          --pt_scaling                      Enable polyT/adapter max detection for read
                                            scaling.
          --pt_median_offset arg            Set polyT median offset for setting read
                                            scaling median (default 2.5)
          --adapter_pt_range_scale arg      Set polyT/adapter range scale for setting
                                            read scaling median absolute deviation
                                            (default 5.2)
          --pt_required_adapter_drop arg    Set minimum required current drop from
                                            adapter max to polyT detection. (default
                                            30.0)
          --pt_minimum_read_start_index arg Set minimum index for read start sample
                                            required to attempt polyT scaling. (default
                                            30)
          -h [ --help ]                     produce help message
          -v [ --version ]                  print version number
          -c [ --config ] arg               Config file to use
          -d [ --data_path ] arg            Path to use for loading any data files the
                                            application requires.
        """

    def __init__(self, client, expected_workers, input_path=None,
                 flowcell=None, kit=None, save_path=None, fast5_out=None,
                 reads_per_fastq=1000, worker_client=None, pull_link=None,
                 image_path=None, bind=None, cpu_threads_per_caller=1):
        self.expected_workers = expected_workers
        self.bind = bind
        self.pull_link = pull_link
        self.image_path = image_path
        self.input_path = Path(input_path)
        self.save_path = save_path
        self.worker_client = worker_client
        self.client = client
        self.command_pattern = self.build_command_pattern(kit=kit, flowcell=flowcell, input_path=input_path, reads_per_fastq=reads_per_fastq, fast5_out=fast5_out)
        self.num_batches = len(os.listdir(str(self.input_path)))
        self.cpu_threads = cpu_threads_per_caller

        self.futures = []

    @property
    def batches(self):
        for batch in os.listdir(str(self.input_path)):
            yield Path(self.save_path).joinpath(batch)

    def build_command_pattern(self, kit=None, flowcell=None, input_path=None, reads_per_fastq=None, fast5_out=False, adapter_trimming=False, cpu_threads_per_caller=1):

        #save_path must be formattable
        save_path = "{save_path}"
        input_path = "{input_path}"

        pattern = "guppy_basecaller --kit {kit} --flowcell {flowcell} --input_path {input_path} --cpu_threads_per_caller {cpu_threads} --save_path {save_path}".format(kit=kit, flowcell=flowcell, cpu_threads=cpu_threads_per_caller, save_path=save_path, input_path=input_path)
        if reads_per_fastq:
            pattern += " --reads_per_fastq {reads_per}".format(reads_per=reads_per_fastq)
        if fast5_out:
            pattern += " --fast5_out"
        if adapter_trimming:
            pattern += " --enable_trimming {}"
        return pattern

    def execute(self):
        dispatched = 0
        dispatch_full = False
        completed_futures = False
        for i in range(self.num_batches):
            try:
                batch = next(self.batches)
            except StopIteration:
                break
            command = self.command_pattern.format(save_path=batch, input_path=self.input_path.joinpath(batch.name))
            future = self.client.submit(singularity_execution, self.worker_client, command.split(" "), self.pull_link, self.image_path, self.bind)
            dispatched += 1

            if completed_futures is False and dispatch_full is False:
                self.futures.append(future)

            if dispatched == self.expected_workers and completed_futures is False:
                completed = as_completed(self.futures)
                completed_futures = True
                dispatch_full = True
            elif dispatch_full and completed_futures:
                completed.add(future)
                dispatched -= 1

                for comp in completed:
                    break
        for comp in completed:
            pass
        collapse_data(self.save_path)


#################################
#Functions for cluster submission
#################################

def basecall(func, command, batch_save_path):
    func(command)
    return batch_save_path
    # except Exception:
    #     print("there is likely a memory problem")
    # return


def singularity_execution(singularity_client, cmd, pull_link=None, image_path=None, bind=None):
    client = SingularityClient()
    if pull_link:
        image = client.pull(image_path)
    else:
        image = image_path
    client.execute(cmd=cmd, image=image, bind=bind)


#################################
# Tooling
#################################

def collapse_data(save_path):
    prep_save_location(save_path)

    seq_sum_paths = []
    config_paths = []
    pipeline_paths = []
    seq_tel_paths = []
    workspace_paths = []

    batches = os.listdir(str(save_path))
    batch_pattern = r'(^)[0-9]+($)'
    for batch in batches:
        if re.match(batch_pattern, batch) == None:
            continue
        batch_path = save_path.joinpath(batch)
        seq_sum_paths.append(str(batch_path.joinpath("sequencing_summary.txt")))
        seq_tel_paths.append(str(batch_path.joinpath("sequencing_telemetry.js")))
        pipeline_paths.append(str(batch_path.joinpath("local_pipeline.yml.log")))
        config_paths.append(str(batch_path.joinpath("configuration.cfg")))
        workspace_paths.append(str(batch_path.joinpath("workspace")))

    collapse_config(config_paths, save_path.joinpath("configuration.cfg"))
    collapse_seq_summary(seq_sum_paths, save_path.joinpath("sequencing_summary.txt"))
    collapse_pipeline(pipeline_paths, save_path.joinpath("local_pipeline.yml.log"))
    collapse_seq_telemetry(seq_tel_paths, save_path.joinpath("sequencing_telemetry.js"))
    collapse_workspace(workspace_paths, save_path.joinpath("workspace"))

    for batch in batches:
        if re.match(batch_pattern, batch) == None:
            continue
        shutil.rmtree(str(save_path.joinpath(batch)))


def collapse_config(config_paths, save_path):
    import numpy as np
    from collections import deque
    config_data = {}
    for config in config_paths:
        row_counter = 0
        with open(str(config), "r") as file:
            for row in file:
                if row == '\n':
                    continue
                if (row, row_counter) in config_data:
                    config_data[(row, row_counter)] += 1

                else:
                    config_data[(row, row_counter)] = 1
                row_counter += 1
                # elif row in config_data and i not in write_rows:
                #     write_rows[i] = [row]
                # else:
                #     config_data[row] = [i]
                #     write_rows[i] = [row]
        file.close()
    print(config_data)
    num_configs = int(len(config_paths) * .90)
    data = {}
    unsure = []

    for d in config_data.keys():
        if config_data[d] >= num_configs:
            data[d[1]] = d[0]
        else:
            unsure.append(d[0])
    print(data)
    with open(str(save_path), 'a') as outfile:
        for i in range(len(config_data)):
            try:
                outfile.write(data[i])
            except:
                pass
        if len(unsure) > 0:
            outfile.write("\n\n##################################\nDiscrepencies in configs\n##################################\n")
            outfile.writelines(unsure)

    return


def collapse_seq_summary(sum_paths, save_path):
    header = None
    with open(str(save_path), 'a') as sum_file:
        for ss in sum_paths:
            with open(ss, "r") as file:
                if header is None:
                    sum_file.writelines(file.readlines())
                    header = True
                else:
                    for i, row in enumerate(file):
                        if i == 0:
                            continue
                        else:
                            sum_file.write(row)

            file.close()
    sum_file.close()
    return


def collapse_seq_telemetry(tel_paths, save_path):
    with open(str(save_path), 'a') as tel_file:
        for tel in tel_paths:
            with open(tel, 'r') as infile:
                tel_file.writelines(infile)
    tel_file.close()
    return


def collapse_pipeline(pipe_paths, save_path):
    with open(str(save_path), 'a') as pipe_file:
        for pipe in pipe_paths:
            with open(pipe, 'r') as infile:
                pipe_file.writelines(infile)
    pipe_file.close()
    return


def collapse_workspace(workspace_paths, save_path):
    counter = 0
    for workspace in workspace_paths:
        for r, d, f in os.walk(str(workspace)):
            dest_root = r.replace(str(workspace), str(save_path))
            for file in f:
                file_name = str(counter) + "_" + file
                src = Path(r).joinpath(file)
                dest = Path(dest_root).joinpath(file_name)
                shutil.move(str(src), str(dest))
                counter += 1


def prep_save_location(save_path):
    save_path = Path(save_path)
    if save_path.joinpath("workspace").exists() is False:
        save_path.joinpath("workspace").mkdir()
    if save_path.joinpath("workspace", "fail").exists() is False:
        save_path.joinpath("workspace", "fail").mkdir()
    if save_path.joinpath("workspace", "pass").exists() is False:
        save_path.joinpath("workspace", "pass").mkdir()
    if save_path.joinpath("workspace", "calibration_strands").exists() is False:
        save_path.joinpath("workspace", "calibration_strands").mkdir()


if __name__ == '__main__':
    configs = ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/9/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/0/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/7/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/6/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/1/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/8/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/4/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/3/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/2/configuration.cfg', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/5/configuration.cfg']
    p = Path('my_test')
    c = Path('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/0/configuration.cfg')
    collapse_config(configs, p)



