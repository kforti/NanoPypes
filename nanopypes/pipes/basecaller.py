from pathlib import Path
import os
import shutil
import datetime
import re

import dask.bag as db
from dask.distributed import wait, as_completed

from nanopypes.pipes.base import Pipe



def batch_generator(batches):
    for batch in batches:
        yield batch


class AlbacoreBasecaller(Pipe):

    def __init__(self, client, albacore, max_batch_size):
        print("Starting the parallel Albacore Basecaller...\n", datetime.datetime.now())
        self.client = client
        self.batch_bunch_size = max_batch_size
        self.albacore = albacore

        # basecaller info
        self.function = albacore.build_func()
        self.input_path = Path(albacore.input_path)
        self.save_path = Path(albacore.save_path)

        self.bc_batches = batch_generator(albacore.batches_for_basecalling)
        self.all_batches = self.albacore.all_batches

        self.futures = []

        # collapse_data
        self.first_summary = True

    def execute(self):
        batch_counter = 0
        with open(str(self.save_path.joinpath("nanopypes_basecall.txt")), "a") as file:
            for batch in self.bc_batches:
                self.futures.append(self.process_batch(batch))
                batch_counter += 1
                if batch_counter == self.batch_bunch_size:
                    break

            completed = as_completed(self.futures)
            for comp in completed:
                try:
                    new_future = self.process_batch(next(self.bc_batches))
                    completed.add(new_future)
                except StopIteration:
                    pass
                completed_batch_path = comp.result()
                file.write(completed_batch_path.name)
                file.write("\n")

            results = self.client.gather(self.futures)

    def process_batch(self, batch):
        batch_save_path = self.save_path.joinpath(batch.name)
        command = self.albacore.build_basecall_command(input_dir=batch)
        bc = self.client.submit(basecall, self.function, command, batch_save_path)
        return bc

    def check_input_data_status(self):
        pass
        #self.client.restart()
        #self.albacore.bc_batches = os.listdir(str(self.save_path))

#################################
#Functions for cluster submission
#################################

def basecall(func, command, batch_save_path):
    func(command)
    return batch_save_path
    # except Exception:
    #     print("there is likely a memory problem")
    # return


#################################
#Utility Functions
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
        pipeline_paths.append(str(batch_path.joinpath("pipeline.log")))
        config_paths.append(str(batch_path.joinpath("configuration.cfg")))
        workspace_paths.append(str(batch_path.joinpath("workspace")))

    collapse_config(config_paths, save_path.joinpath("configuration.cfg"))
    collapse_seq_summary(seq_sum_paths, save_path.joinpath("sequencing_summary.txt"))
    collapse_pipeline(pipeline_paths, save_path.joinpath("pipeline.log"))
    collapse_seq_telemetry(seq_tel_paths, save_path.joinpath("sequencing_telemetry.js"))
    collapse_workspace(workspace_paths, save_path.joinpath("workspace"))


def collapse_config(config_paths, save_path):
    config_data = []
    config_bag = db.read_text(config_paths)
    for row in config_bag.compute():
        if row not in config_data:
            config_data.append(row)

    with open(str(save_path), 'a') as config:
        config.writelines(config_data)
    config.close()


def collapse_seq_summary(sum_paths, save_path):
    header = None
    seq_sum_bag = db.read_text(sum_paths)
    with open(str(save_path), 'a') as sum_file:
        for seq in seq_sum_bag.compute():
            if header == None:
                header = seq
            elif seq == header:
                continue
            sum_file.write(seq)
    sum_file.close()
    return


def collapse_seq_telemetry(tel_paths, save_path):
    seq_sum_bag = db.read_text(tel_paths)
    with open(str(save_path), 'a') as tel_file:
        for seq in seq_sum_bag.compute():
            tel_file.write(seq)
    tel_file.close()
    return


def collapse_pipeline(pipe_paths, save_path):
    pipe_bag = db.read_text(pipe_paths)
    with open(str(save_path), 'a') as pipe_file:
        for seq in pipe_bag.compute():
            pipe_file.write(seq)
    pipe_file.close()
    return


def collapse_workspace(workspace_paths, save_path):
    for workspace in workspace_paths:
        for r, d, f in os.walk(str(workspace)):
            dest_root = r.replace(str(workspace), str(save_path))
            for file in f:
                src = Path(r).joinpath(file)
                dest = Path(dest_root).joinpath(file)
                shutil.move(str(src), str(dest))

def prep_save_location(save_path):
    save_path = Path(save_path)
    if save_path.joinpath("workspace").exists() == False:
        save_path.joinpath("workspace").mkdir()
    if save_path.joinpath("workspace", "fail").exists() == False:
        save_path.joinpath("workspace", "fail").mkdir()
    if save_path.joinpath("workspace", "pass").exists() == False:
        save_path.joinpath("workspace", "pass").mkdir()
    if save_path.joinpath("workspace", "calibration_strands").exists() == False:
        save_path.joinpath("workspace", "calibration_strands").mkdir()

