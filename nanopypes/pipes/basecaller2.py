from pathlib import Path
import os
import shutil
import datetime

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
                print("processing batch: ", batch.name)
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
