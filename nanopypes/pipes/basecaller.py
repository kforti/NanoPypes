from pathlib import Path
import os
import shutil
import datetime
import re
import sys

import dask
from dask.distributed import fire_and_forget

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

    def __init__(self, client, albacore, num_splits, batch_bunch_size):
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
        self.all_batches = albacore.batches
        self.batch_bunches = batch_generator(self.all_batches, batch_bunch_size)
        self.all_basecalls = []

        #graphs
        self.all_basecalls = []
        self.all_data_collapse = []

    def execute(self):
        for batch_bunch in self.batch_bunches:
            print("processing batch bunch: ", batch_bunch)
            for batch in batch_bunch:
             #   print("processing batch: ", batch)
                self.build_graphs(batch)
            #print("gathering basecalls")
            completed_basecalls = 0
            total_basecalls = self.num_splits * self.batch_bunch_size
            # while completed_basecalls < total_basecalls:
            #     for future in self.all_basecalls:
            #         if future.done():
            #             del future
            #             completed_basecalls += 1
            #
            # self.client.gather(self.all_basecalls)
            # self.all_basecalls = []
            while True:
                user_input = input("Continue to next batch?")
                if user_input == 'yes':
                    break

            #TODO: remove split_data dir


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
            split_save_path = self.save_path.joinpath(batch.name)
            if this_split_path.exists() == False:
                try:
                    this_split_path.mkdir()
                except Exception as e:
                    pass
            #print("submitting copy_files")
            copy_files = self.client.submit(copy_splits, split_paths, this_split_path, priority=-10)
            #print("submitting commands")
            commands = self.client.submit(get_command, i, batch.name, self.albacore.build_command, self.input_path, None, priority=-10)
            #print("submitting basecalls")
            bc = self.client.submit(basecall, self.function, commands, [copy_files, commands], priority=10)
            rm_splits = self.client.submit(remove_splits, this_split_path, [bc], priority=-10)
            fire_and_forget(rm_splits)

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


#####################
# Dask Functions
# Basecall Graphs
#####################



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


if __name__ == '__main__':

    pass
