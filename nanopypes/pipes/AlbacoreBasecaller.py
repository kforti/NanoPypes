from pathlib import Path
from copy import copy
import os
import math
import shutil

import dask
import dask.dataframe as dd

import pandas as pd
from nanopypes.pipes.base import Pipe


class AlbacoreBasecall(Pipe):
    def __init__(self, albacore, data_splits, client):
        print("Configuring albacore pipe.... ")
        self.albacore = albacore
        self.client = client

        self.func = self.albacore.build_func()
        self.input_path = Path(self.albacore.input_path)
        self.save_path = Path(self.albacore.save_path)
        self.splits_paths = []
        self.batch_splits = data_splits


    def execute(self):
        batch_counter = 0
        batches = len(self.albacore.batches)
        results = []

        for batch in self.albacore.batches:
            chunk_size = math.ceil((len(os.listdir(self.input_path.joinpath(batch.name))) / self.batch_splits))
            split_data = self.split_data(batch.name, self.input_path, chunk_size)
            commands = self.get_commands(self.batch_splits, batch.name, self.albacore, self.input_path)
            results.append((split_data, commands))
        return results


    def remove_parallel_data(self, path=None):
        if path == None:
            path = self.save_path
        batch_pattern = r'(^)[0-9]+($)'
        for batch in os.listdir(str(self.save_path)):
            if re.match(batch_pattern, batch):
                shutil.rmtree(str(self.save_path.joinpath(batch)))
            else:
                continue

    @dask.delayed
    def split_data(self, batch, input_path, chunk_size):
        batch = copy(batch)
        input_path = Path(input_path)
        chunk_size = copy(chunk_size)

        batch_path = input_path.joinpath(batch)
        num_files = len(os.listdir(str(batch_path)))
        file_counter = 0
        all_files = []
        chunk = []
        for i, file in enumerate(os.listdir(str(batch_path))):
            file_counter += 1
            chunk.append(batch_path.joinpath(file))
            if file_counter == chunk_size or i == num_files:
                file_counter.append(chunk)
                chunk = []
                file_counter = 0
        return all_files

    @dask.delayed
    def get_commands(self, splits, batch_name, albacore, input_path):
        splits = copy(splits)
        batch_name = copy(batch_name)
        albacore = copy(albacore)
        input_path = copy(input_path)

        commands = []
        for split in range(splits):
            commands.append(albacore.build_command(str(input_path.joinpath(batch_name, 'split_data', str(split))), batch_name))
        return commands

    def __call__(self):
        self.client.compute(self.execute())

def mv_reads_function(batch, save_path):

    def mv_reads(split, batch=batch, save_path=save_path):
        split_path = save_path.joinpath(batch, str(split))
        print(split_path)
        for read_type in os.listdir(str(split_path.joinpath('workspace'))):
            print(read_type)
            if save_path.joinpath('workspace', read_type).exists() == False:
                try:
                    save_path.joinpath('workspace', read_type).mkdir()
                except FileExistsError:
                    pass

            for barcode in os.listdir(str(split_path.joinpath('workspace', read_type))):
                print(barcode)
                if save_path.joinpath('workspace', read_type, barcode).exists() == False:
                    try:
                        save_path.joinpath('workspace', read_type, barcode).mkdir()
                    except FileExistsError:
                        pass

                for read in os.listdir(str(split_path.joinpath('workspace', read_type, barcode))):
                    print("movings reads... ", str(split_path.joinpath('workspace', read_type, barcode, read)), str(save_path.joinpath('workspace', read_type, barcode, read)))
                    shutil.move(str(split_path.joinpath('workspace', read_type, barcode, read)), str(save_path.joinpath('workspace', read_type, barcode, read)))
    return mv_reads



@dask.delayed
def get_split_paths(batch, chunk_size):
    batch = copy(batch)
    chunk_size = copy(chunk_size)

    files = os.listdir(str(batch))
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

@dask.delayed
def copy_splits(splits, split_path, split_data):
    splits = copy(splits)
    split_path = copy(split_path)
    for file in splits:
        new_file_path = split_path.joinpath(file.name)
        try:
            shutil.copyfile(str(file), str(new_file_path))
        except Exception as e:
            return (str(file), str(new_file_path))

    return

@dask.delayed
def get_command(split, batch_name, build_command, input_path, splt_data):
    split = copy(split)
    batch_name = copy(batch_name)
    build_command = copy(build_command)
    input_path = copy(input_path)
    command = build_command(str(input_path.joinpath(batch_name, 'split_data', str(split))), batch_name)
    return command

@dask.delayed
def basecall(func, command):
    return func(command)

@dask.delayed
def digest_telemetry(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    return data

@dask.delayed
def digest_summary(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    return data

@dask.delayed
def digest_pipeline(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    return data

@dask.delayed
def digest_configuration(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)

    return data

@dask.delayed
def digest_workspace(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    for read_type in os.listdir(str(path)):

        if save_path.joinpath(read_type).exists() == False:
            try:
                save_path.joinpath(read_type).mkdir()
            except FileExistsError:
                pass

        for barcode in os.listdir(str(path.joinpath(read_type))):
            if save_path.joinpath(read_type, barcode).exists() == False:
                try:
                    save_path.joinpath(read_type, barcode).mkdir()
                except FileExistsError:
                    pass

            for read in os.listdir(str(path.joinpath(read_type, barcode))):
                shutil.move(str(path.joinpath(read_type, barcode, read)),
                            str(save_path.joinpath(read_type, barcode, read)))
    return

@dask.delayed
def sum_results(tel, summ, conf, pipe, wrkspc):
    results = {'telemetry': tel,
               'summary': summ,
               'config': conf,
               'pipe': pipe,
               'workspace': wrkspc}
    return results


def write_data(data, save_path):
    with open(str(save_path), 'a') as file:
        for batch in data:
            for split in batch:
                for row in split:
                    file.write(row)
    return

def write_config(data, save_path):
    first_config = True
    final_config_data = []
    with open(str(save_path), 'a') as file:
        for batch in data:
            for split in batch:
                if split in final_config_data:
                    continue
                else:
                    final_config_data.append(split)

                for row in split:
                    file.write(row)

    return

def write_summary(data, save_path):
    header = True
    with open(str(save_path), 'a') as file:
        for batch_bunch in data:
            for batch in batch_bunch:
                for split in batch:
                    for i, row in enumerate(split):
                        if header == False and i == 0:
                            continue
                        else:
                            file.write(row)
                            if header:
                                header = False
    return

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

def prep_save_path(save_path):
    if save_path.joinpath('sequencing_telemetry.js').exists() == False:
        save_path.joinpath('sequencing_telemetry.js').touch()
    if save_path.joinpath('sequencing_summary.txt').exists() == False:
        save_path.joinpath('sequencing_summary.txt').touch()
    if save_path.joinpath('pipeline.log').exists() == False:
        save_path.joinpath('pipeline.log').touch()
    if save_path.joinpath('configuration.cfg').exists() == False:
        save_path.joinpath('configuration.cfg').touch()
    if save_path.joinpath('workspace').exists() == False:
        save_path.joinpath('workspace').mkdir()


def start(albacore, client, data_splits, batch_bunch_size):
    print("Starting the parallel Albacore Basecaller...")
    func = albacore.build_func()
    input_path = Path(albacore.input_path)
    save_path = Path(albacore.save_path)
    build_command = albacore.build_command
    num_splits = data_splits
    all_batches = albacore.batches
    num_batches = len(all_batches)
    batch_bunches = batch_generator(all_batches, batch_bunch_size)
    final_results = {'summary': [],
                     'telemetry': [],
                     'config': [],
                     'pipe': []}

    prep_save_path(save_path)
    batch_chunk_counter = 0
    for batch_bunch in batch_bunches:
        print("Creating the compute graph for batches: ", (1 + batch_chunk_counter * num_batches), " - ", (batch_chunk_counter + 1) * num_batches)
        batch_chunk_counter += 1
        graph = get_graph(save_path, func, build_command, input_path, num_splits, batch_bunch)
        # graph.visualize()
        futures = client.compute(graph)
        results = client.gather(futures)
        final_results['summary'].append(results['summary'])
        final_results['telemetry'].append(results['telemetry'])
        final_results['config'].append(results['config'])
        final_results['pipe'].append(results['pipe'])

    write_summary(final_results['summary'], albacore.save_path.joinpath('sequencing_summary.txt'))
    write_data(final_results['telemetry'], albacore.save_path.joinpath('sequencing_telemetry.js'))
    write_config(final_results['config'], albacore.save_path.joinpath('configuration.cfg'))
    write_data(final_results['pipe'], albacore.save_path.joinpath('pipeline.log'))

    return results

def get_graph(save_path, func, build_command, input_path, batch_splits, batches):
    commands = []
    basecalls = []

    batch_telemetries = []
    batch_summaries = []
    batch_pipelines = []
    batch_configs = []
    batch_workspaces = []

    for batch in batches:
        split_path = input_path.joinpath(batch.name, 'split_data')
        if split_path.exists() == False:
            try:
                split_path.mkdir()
            except Exception as e:
                pass
        chunk_size = int((len(os.listdir(str(batch))) / batch_splits))
        spl_data = get_split_paths(batch, chunk_size)

        split_summaries = []
        split_pipelines = []
        split_telemetries = []
        split_configs = []
        split_workspaces = []
        for split in range(batch_splits):
            this_split_path = split_path.joinpath(str(split))
            if this_split_path.exists() == False:
                try:
                    this_split_path.mkdir()
                except Exception as e:
                    pass
            copy_files = copy_splits(spl_data[split], this_split_path, spl_data)

            command = get_command(split, batch.name, build_command, input_path, copy_files)
            commands.append(command)

            bc = basecall(func, command)
            basecalls.append(bc)

            split_save_path = save_path.joinpath(batch.name)

            telemetry = digest_telemetry(split_save_path.joinpath(str(split), 'sequencing_telemetry.js'), split_save_path.joinpath('sequencing_telemetry.js'), bc)
            summary = digest_summary(split_save_path.joinpath(str(split), 'sequencing_summary.txt'), split_save_path.joinpath('sequencing_summary.txt'), bc)
            pipeline = digest_pipeline(split_save_path.joinpath(str(split), 'pipeline.log'), split_save_path.joinpath('pipeline.log'), bc)
            configuration = digest_configuration(split_save_path.joinpath(str(split), 'configuration.cfg'), split_save_path.joinpath('configuration.cfg'), bc)
            workspace = digest_workspace(save_path.joinpath(batch.name, str(split), 'workspace'), save_path.joinpath('workspace'), bc)
            split_summaries.append(summary)
            split_telemetries.append(telemetry)
            split_pipelines.append(pipeline)
            split_configs.append(configuration)
            split_workspaces.append(workspace)

        batch_summaries.append(split_summaries)
        batch_pipelines.append(split_pipelines)
        batch_telemetries.append(split_telemetries)
        batch_configs.append(split_configs)
        batch_workspaces.append(split_workspaces)

    results = sum_results(summ=batch_summaries, tel=batch_telemetries, pipe=batch_pipelines, conf=batch_configs, wrkspc=batch_workspaces)
    return results



