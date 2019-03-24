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
def split_data(batch, chunk_size):
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
def copy_splits(splits, split_path):
    for file in splits:

        new_file_path = split_path.joinpath(file.name)
        try:
            shutil.copyfile(str(file), new_file_path)
        except Exception as e:
            return e

    return

@dask.delayed
def digest_telemetry(path, bc):
    path = copy(path)
    df = dd.read_json(path)
    return df

@dask.delayed
def digest_summary(path, bc):
    path = copy(path)
    df = dd.read_csv(path)
    return df

@dask.delayed
def digest_pipeline(path, bc):
    path = copy(path)
    df = dd.read_fwf(path)
    return df

@dask.delayed
def digest_configuration(path, bc):
    path = copy(path)
    df = dd.read_fwf(path)
    return df

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
    return (tel, summ, conf, pipe, wrkspc)

@dask.delayed
def append_dfs(df, num_dfs):
    df = copy(df)
    summed_df = df[0]

    for i in range(num_dfs):
        if i == 0:
            continue
        return summed_df.append(df[i])#, ignore_index=True)#, lsuffix='_caller', rsuffix='_other')


@dask.delayed
def write_csv(path, df, name):
    df = copy(df)
    path = copy(path)
    name = copy(name)
    save_name = path.joinpath((name + '*.csv'))
    df.to_csv(save_name)
    os.rename(str(path.joinpath((name + '*.csv'))), str(path.joinpath(name)))
    return df

@dask.delayed
def write_json(path, df, name):
    df = copy(df)
    path = copy(path)
    name = copy(name)
    df.to_json(path)
    os.rename(str(path.joinpath('*.part')), str(path.joinpath(name)))
    return df

@dask.delayed
def write_fwf(path, df, name):
    df = copy(df)
    path = copy(path)
    name = copy(name)
    df.to_fwf(path)
    os.rename(str(path.joinpath('0.part')), str(path.joinpath(name)))
    return df

def start(albacore, client, data_splits):
    func = albacore.build_func()
    input_path = Path(albacore.input_path)
    save_path = Path(albacore.save_path)
    splits_paths = []
    batch_splits = data_splits

    graph = get_graph(albacore, input_path, batch_splits)
    graph.visualize()
    futures = client.compute(graph)
    results = client.gather(futures)
    return results

def get_graph(albacore, input_path, batch_splits):
    batch_counter = 0
    batches = len(albacore.batches)
    save_path = albacore.save_path
    results = []
    build_command = albacore.build_command
    func = albacore.build_func()
    commands = []
    basecalls = []

    batch_telemetries = []
    batch_summaries = []
    batch_pipelines = []
    batch_configs = []
    batch_workspaces = []

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

    for batch in albacore.batches:
        split_path = input_path.joinpath(batch.name, 'split_data')
        if split_path.exists() == False:
            try:
                split_path.mkdir()
            except Exception as e:
                pass
        chunk_size = int((len(os.listdir(str(batch))) / batch_splits))
        print("chunk size.... ", chunk_size)
        spl_data = split_data(batch, chunk_size)

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
            copy_files = copy_splits(spl_data[split], this_split_path)

            command = get_command(split, batch.name, build_command, input_path, spl_data)
            commands.append(command)

            bc = basecall(func, command)
            basecalls.append(bc)

            telemetry = digest_telemetry(save_path.joinpath(batch.name, str(split), 'sequencing_telemetry.js'), bc)
            summary = digest_summary(save_path.joinpath(batch.name, str(split), 'sequencing_summary.txt'), bc)
            pipeline = digest_pipeline(save_path.joinpath(batch.name, str(split), 'pipeline.log'), bc)
            configuration = digest_configuration(save_path.joinpath(batch.name, str(split), 'configuration.cfg'), bc)
            workspace = digest_workspace(save_path.joinpath(batch.name, str(split), 'workspace'), save_path.joinpath('workspace'), bc)
            split_summaries.append(summary)
            split_telemetries.append(telemetry)
            split_pipelines.append(pipeline)
            split_configs.append(configuration)
            split_workspaces.append(workspace)
        batch_summary = append_dfs(split_summaries, batch_splits)
        batch_summaries.append(batch_summary)
        batch_pipeline = append_dfs(split_pipelines, batch_splits)
        batch_pipelines.append(batch_pipeline)
        batch_telemetry = append_dfs(split_telemetries, batch_splits)
        batch_telemetries.append(batch_telemetry)
        batch_config = append_dfs(split_configs, batch_splits)
        batch_configs.append(batch_config)
        batch_workspaces.append(split_workspaces)

    final_summary = append_dfs(batch_summaries, batches)
    final_telemetry = append_dfs(batch_telemetries, batches)
    final_pipeline = append_dfs(batch_pipelines, batches)
    final_config = append_dfs(batch_configs, batches)

    summary_result = write_csv(save_path, final_summary, 'sequencing_summary.txt')
    telemetry_result = write_json(save_path, final_telemetry, 'sequencing_telemetry.js')
    pipeline_result = write_csv(save_path, final_pipeline, 'pipeline.log')
    config_result = write_csv(save_path, final_config, 'configuration.cfg')
    results = sum_results(summ=summary_result, tel=telemetry_result, pipe=pipeline_result, conf=config_result, wrkspc=batch_workspaces)
    return results



if __name__ == '__main__':
    # telemetry1 = digest_telemetry('/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/basecalled_data/results/local_basecall_test/7/0/sequencing_telemetry.js', None)
    # telemetry2 = digest_telemetry('/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/basecalled_data/results/local_basecall_test/7/1/sequencing_telemetry.js', None)
    # telemetry3 = digest_telemetry('/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/basecalled_data/results/local_basecall_test/7/2/sequencing_telemetry.js', None)
    # tocsv = telemetry1.to_csv('tel1*.csv')
    # tel1 = tocsv.compute()
    #
    # tels = [telemetry1, telemetry2, telemetry3]
    # merger = append_dfs(tels, 3)
    # # final = merger.drop_duplicates()
    # result = merger.to_csv('final*.csv')
    # result.compute()
   
