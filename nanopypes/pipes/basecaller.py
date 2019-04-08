from pathlib import Path
import os
import shutil
import datetime
import time
import re
import sys
from asyncio.futures import CancelledError

import dask
import dask.bag as db
from dask.distributed import fire_and_forget, wait, as_completed, futures_of

from nanopypes.pipes.base import Pipe



def batch_generator(batches, batch_size):
    batches_len = len(batches)
    batch_counter = 0
    return_batches = []
    for i, batch in enumerate(batches):
        return_batches.append(batch)
        batch_counter += 1
        if batch_counter == batch_size or i + 1 == batches_len:
            yield return_batches
            return_batches = []
            batch_counter = 0


def copy_splits(splits, split_path):
    for file in splits:
        new_file_path = split_path.joinpath(file.name)
        try:
            shutil.copyfile(str(file), str(new_file_path))
        except Exception as e:
            return (str(file), str(new_file_path))

    return


class AlbacoreBasecaller(Pipe):

    def __init__(self, client, albacore, num_splits, batch_bunch_size, continue_on):
        print("Starting the parallel Albacore Basecaller...\n", datetime.datetime.now())
        self.client = client
        self.num_splits = num_splits
        self.batch_bunch_size = batch_bunch_size
        self.albacore = albacore

        # basecaller info
        self.barcoding = albacore.barcoding
        self.output_format = albacore.output_format
        self.function = albacore.build_func()
        self.input_path = Path(albacore.input_path)
        self.save_path = Path(albacore.save_path)

        if continue_on:
            self.albacore.bc_batches = self.prep_data()
            self.client.restart()

        self.bc_batches = albacore.batches_for_basecalling
        self.bc_batch_bunches = batch_generator(self.bc_batches, batch_bunch_size)
        self.all_batches = self.albacore.all_batches

        #graphs
        self.all_basecalls = []
        self.all_data_collapse = []

        self.futures = []

        self.first_summary = True

    def execute(self):
        self.basecall()

        self.collapse_data()

    def basecall(self):
        # Perform parallel basecall
        for batch_bunch in self.bc_batch_bunches:
            print("processing batch bunch: ", batch_bunch)
            for batch in batch_bunch:
                self.build_graphs(batch)

            comp = as_completed(self.futures)
            tasks = 0
            for comlpeted_future in comp:
                try:
                    self.client.cancel(comlpeted_future)
                    tasks += 1
                    if tasks > (self.batch_bunch_size * self.num_splits * .7):
                        break
                except StopIteration:
                    break
        wait(self.futures)
        # TODO: remove split_data dir
        self.client.map(self.shutil.rmtree, [str(self.input_path.joinpath(batch, 'split_data')) for batch in os.listdir(str(self.input_path))])

    def collapse_data(self):
        self.get_read_id()
        print(str(self.save_path))
        collapse_batches = batch_generator(os.listdir(str(self.save_path)), 5)
        self._prep_save_location()

        for i, bunch in enumerate(collapse_batches):
            print("bunch")
            read_paths = self.get_read_paths(bunch)
            self.write_reads(read_paths)
            file_paths = self.get_file_paths(bunch)
            print("file paths", file_paths)
            if i == 0:
                self.write_config(file_paths['configs'])
            self.write_summary(file_paths['summaries'])
            self.write_telemetry(file_paths['telemetries'])
            self.write_pipeline(file_paths['pipelines'])

    def build_graphs(self, batch):
        spl_data = self.get_split_paths(batch)
        split_path = self.input_path.joinpath(batch.name, 'split_data')
        if split_path.exists() == False:
            try:
                split_path.mkdir()
            except Exception as e:
                raise IOError("There is already a split_data directory in the ", batch.name, " directory")

        chunk_size = int((len(os.listdir(str(batch))) / self.num_splits))

        for i, split_paths in enumerate(spl_data):
            #print("processing split paths: ", split_paths)
            this_split_path = split_path.joinpath(str(i))

            if this_split_path.exists() == False:
                try:
                    this_split_path.mkdir()
                except Exception as e:
                    pass

            copy_files = self.client.submit(copy_splits, split_paths, this_split_path, priority=-10)
            commands = self.client.submit(get_command, i, batch.name, self.albacore.build_command, self.input_path, None, priority=-10)
            bc = self.client.submit(basecall, self.function, commands, [copy_files, commands], priority=10)
            rm_splits = self.client.submit(remove_splits, this_split_path, [bc], priority=0)
            self.futures.append(rm_splits)

    def get_split_paths(self, batch):
        files = os.listdir(str(batch))
        chunk_size = int(len(files) / self.num_splits)
        file_counter = 0
        all_files = []
        chunk = []
        for i, file in enumerate(files):
            file_counter += 1
            chunk.append(batch.joinpath(file))
            if file_counter == chunk_size or i == len(files):
                all_files.append(chunk)
                chunk = []
                file_counter = 0
        return all_files

    def prep_data(self):
        print("Prepping data from previously stopped run")
        bc_batches = os.listdir(str(self.save_path))
        final_bc_batches = []
        all_futures = []
        for batch in os.listdir(str(self.input_path)):
            if batch in bc_batches:
               # print("batch ", batch, " is in bc_batches")
                if len(os.listdir(str(self.input_path.joinpath(batch, 'split_data')))) > 0:
                    #print("Removing data: ", batch)
                    save_future = self.client.submit(shutil.rmtree, str(self.save_path.joinpath(batch)))
                    split_future = self.client.submit(shutil.rmtree, str(self.input_path.joinpath(batch, 'split_data')))
                    all_futures.append(save_future)
                    all_futures.append(split_future)
            else:
                #print("Batch: ", batch, " ok!")
                final_bc_batches.append(batch)
        wait(all_futures)
        del all_futures
        return final_bc_batches

    def _prep_save_location(self):
        if self.save_path.joinpath("workspace").exists() == False:
            self.save_path.joinpath("workspace").mkdir()
        if self.save_path.joinpath("workspace", "fail").exists() == False:
            self.save_path.joinpath("workspace", "fail").mkdir()
        if self.save_path.joinpath("workspace", "pass").exists() == False:
            self.save_path.joinpath("workspace", "pass").mkdir()
        if self.save_path.joinpath("workspace", "calibration_strands").exists() == False:
            self.save_path.joinpath("workspace", "calibration_strands").mkdir()

    def get_read_paths(self, bunch):
        read_paths = {}
        read_paths['pass'] = [str(self.save_path.joinpath(batch, str(split), "workspace", "pass", self.read_id)) for split in range(self.num_splits) for batch in bunch if self.save_path.joinpath(batch, str(split), "workspace", "pass").exists()]
        read_paths['fail'] = [str(self.save_path.joinpath(batch, str(split), "workspace", "fail", self.read_id)) for
                          split in range(self.num_splits) for batch in bunch if self.save_path.joinpath(batch, str(split), "workspace", "fail").exists()]
        read_paths['calibration_strands'] = [str(self.save_path.joinpath(batch, str(split), "workspace", "calibration_strands", self.read_id)) for
                          split in range(self.num_splits) for batch in bunch if self.save_path.joinpath(batch, str(split), "workspace", "calibration_strands").exists()]

        return read_paths

    def get_file_paths(self, bunch):
        file_paths = {}
        file_paths['configs'] = [str(self.save_path.joinpath(batch, str(split), "configuration.cfg")) for split in range(self.num_splits) for batch in bunch]
        file_paths['summaries'] = [str(self.save_path.joinpath(batch, str(split), "sequencing_summary.txt")) for split in range(self.num_splits) for batch in bunch]
        file_paths['telemetries'] = [str(self.save_path.joinpath(batch, str(split), "sequencing_telemetry.js")) for split in range(self.num_splits) for batch in bunch]
        file_paths['pipelines'] = [str(self.save_path.joinpath(batch, str(split), "pipeline.log")) for split in range(self.num_splits) for batch in bunch]

        return file_paths

    def write_reads(self, read_paths):
        with open(str(self.save_path.joinpath("workspace", "pass", self.read_id)), "a") as file:
            file.writelines(db.read_text(read_paths['pass']).compute())
            file.close()
        with open(str(self.save_path.joinpath("workspace", "fail", self.read_id)), "a") as file:
            file.writelines(db.read_text(read_paths['fail']).compute())
            file.close()
        with open(str(self.save_path.joinpath("workspace", "calibration_strands", self.read_id)), "a") as file:
            file.writelines(db.read_text(read_paths['calibration_strands']).compute())
            file.close()

    def write_config(self, config_paths):
        with open(config_paths[0], 'r') as config:
            config_data = [line for line in config]
            config.close()
            with open(str(self.save_path.joinpath("configuration.cfg")), 'a') as file:
                file.writelines(config_data)
                file.close()

    def write_summary(self, summary_paths):
        with open(str(self.save_path.joinpath("sequencing_summary.txt")), 'a') as file:
            if self.first_summary:
                for i, read in enumerate(db.read_text(summary_paths).compute()):
                    if i == 0:
                        self.summary_header = read
                        file.write(read)
                    else:
                        if read == self.summary_header:
                            continue
                        file.write(read)
                file.close()
                self.first_summary = False

            else:
                for i, read in enumerate(db.read_text(summary_paths).compute()):
                    if read == self.summary_header:
                        continue
                    file.write(read)
                file.close()

    def write_telemetry(self, telemetry_paths):
        with open(str(self.save_path.joinpath("sequencing_telemetry.js")), 'a') as file:
            file.writelines(db.read_text(telemetry_paths).compute())
            file.close()

    def write_pipeline(self, pipeline_paths):
        with open(str(self.save_path.joinpath("pipeline.log")), 'a') as file:
            file.writelines(db.read_text(pipeline_paths).compute())
            file.close()

    def get_read_id(self):
        #Just need 1 read name, but no hardcoding to prevent failing
        for batch in os.listdir(str(self.save_path)):
            for split in os.listdir(str(self.save_path.joinpath(batch))):
                for read_type in os.listdir(str(self.save_path.joinpath(batch, split, "workspace"))):
                    for read in os.listdir(str(self.save_path.joinpath(batch, split, "workspace", read_type))):
                        self.read_id = read
                        return

#######################
#Distributed Functions#
#TODO: could probably be integrated directly into the albacorecore basecaller class
#######################

def get_command(split, batch_name, build_command, input_path, dependencies):
    command = build_command(str(input_path.joinpath(batch_name, 'split_data', str(split))), batch_name)
    return command


def basecall(func, command, dependencies):
    try:
        func(command)
    except Exception:
        print("there is likely a memory problem")
    return


def remove_splits(split_path, dependencies):
    try:
        shutil.rmtree(str(split_path))
    except FileNotFoundError as e:
        pass
    return

