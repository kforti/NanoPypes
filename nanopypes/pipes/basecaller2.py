from pathlib import Path
import os
import shutil
import datetime

import dask.bag as db
from dask.distributed import wait, as_completed

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
        for batch_bunch in self.bc_batches:
            for batch in batch_bunch:
                command = self.albacore.build_command(input_dir=str(batch), batch_number=None,
                                                       save_path=str(self.save_path.joinpath(batch.name)))
                bc = self.client.submit(basecall, self.function, command, dependencies=None)
                self.futures.append(bc)
            wait(self.futures)

def basecall(func, command, dependencies):
    try:
        func(command)
    except Exception:
        print("there is likely a memory problem")
    return
