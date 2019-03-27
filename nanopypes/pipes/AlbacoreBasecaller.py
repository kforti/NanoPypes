from pathlib import Path
from copy import copy
import os
import math
import shutil

import dask
import dask.bag as db

import pandas as pd
from nanopypes.pipes.base import Pipe

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
def remove_splits(batch, dependencies):
    batch = copy(batch)
    shutil.rmtree(str(batch))
    return

@dask.delayed
def digest_splits(rm_splits):
    return rm_splits

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
    infile.close()
    return data

@dask.delayed
def digest_summary(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    infile.close()
    return data

@dask.delayed
def digest_pipeline(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    infile.close()
    return data

@dask.delayed
def digest_configuration(path, save_path, bc):
    path = copy(path)
    save_path = copy(save_path)
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    infile.close()
    return data

@dask.delayed
def digest_fast5_workspace(path, save_path, barcoding, bc):
    path = copy(path)
    save_path = copy(save_path)
    for read_type in os.listdir(str(path)):
        if save_path.joinpath(read_type).exists() == False:
            try:
                save_path.joinpath(read_type).mkdir()
            except FileExistsError:
                pass

        if barcoding and read_type != 'calibration_strands':
            for barcode in os.listdir(str(path.joinpath(read_type))):
                if save_path.joinpath(read_type, barcode).exists() == False:
                    try:
                        save_path.joinpath(read_type, barcode).mkdir()
                    except FileExistsError:
                        pass
                for bcode_batch in os.listdir(str(path.joinpath(read_type, barcode))):
                    if save_path.joinpath(read_type, barcode, bcode_batch).exists() == False:
                        try:
                            save_path.joinpath(read_type, barcode, bcode_batch).mkdir()
                        except FileExistsError:
                            pass
                    for read in os.listdir(str(path.joinpath(read_type, barcode, bcode_batch))):
                        shutil.move(str(path.joinpath(read_type, barcode, bcode_batch, read)),
                                    str(save_path.joinpath(read_type, barcode, bcode_batch, read)))

        elif barcoding == False or read_type == 'calibration_strands':
            for rt_batch in os.listdir(str(path.joinpath(read_type))):
                if save_path.joinpath(read_type, rt_batch).exists() == False:
                    try:
                        save_path.joinpath(read_type, rt_batch).mkdir()
                    except FileExistsError:
                        pass
                for read in os.listdir(str(path.joinpath(read_type, rt_batch))):
                    shutil.move(str(path.joinpath(read_type, rt_batch, read)),
                                str(save_path.joinpath(read_type, rt_batch, read)))
    return

@dask.delayed
def digest_fastq_workspace(path, save_path, barcoding, bc):
    path = copy(path)
    save_path = copy(save_path)
    for read_type in os.listdir(str(path)):
        if save_path.joinpath(read_type).exists() == False:
            try:
                save_path.joinpath(read_type).mkdir()
            except FileExistsError:
                pass
        if barcoding and read_type != 'calibration_strands':
            for barcode in os.listdir(str(path.joinpath(read_type))):
                if save_path.joinpath(read_type, barcode).exists() == False:
                    try:
                        save_path.joinpath(read_type, barcode).mkdir()
                    except FileExistsError:
                        pass
                for read in os.listdir(str(path.joinpath(read_type, barcode))):
                    shutil.move(str(path.joinpath(read_type, barcode, read)),
                                str(save_path.joinpath(read_type, barcode, read)))

        elif barcoding == False or read_type == 'calibration_strands':
            for read in os.listdir(str(path.joinpath(read_type))):
                shutil.move(str(path.joinpath(read_type, read)),
                                str(save_path.joinpath(read_type, read)))
    return

@dask.delayed
def digest_all_workspaces(workspace):
    return workspace

@dask.delayed
def digest_all_configurations(configs):
    return configs

#@dask.delayed
def sum_results(tel, summ, conf, pipe, wrkspc, rm_splits):
    results = {'telemetry': tel,
               'summary': summ,
               'config': conf,
               'pipe': pipe,
               'workspace': wrkspc,
               'rm_splits': rm_splits}
    return results


def write_data(data, save_path):
    with open(str(save_path), 'a') as file:
        for row in data:
            file.write(row)
    file.close()
    return

def write_config(data, save_path):
    final_config_data = []
    with open(save_path, 'r') as file:
        for line in file:
            final_config_data.append(line)
    file.close()
    for bunch in data:
        for row in bunch:
            if row not in final_config_data:
                final_config_data.append(row)
            else:
                continue
    with open(str(save_path), 'w') as file2:
        for row in final_config_data:
            file2.write(row)
    file2.close()
    return

def write_summary(data, save_path):
    first_row = None
    with open(save_path, 'a') as file:
        for row in data:
            if first_row == None:
                first_row = row
                file.write(row)
            elif first_row:
                if row == first_row:
                    continue
                file.write(row)

    file.close()
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

    prep_save_path(save_path)
    batch_chunk_counter = 0
    for batch_bunch in batch_bunches:
        bunches_name = "Processing Batches " + str((1 + batch_chunk_counter * batch_bunch_size)) + "-" + str((batch_chunk_counter + 1) * batch_bunch_size)
        print(bunches_name)
        print("Creating the Compute Graph ")
        graph = get_graph(save_path, func, build_command, input_path, num_splits, batch_bunch, albacore.barcoding, albacore.output_format)
        for key in graph.keys():
            graph[key].visualize()

        print("Computing the Graph ")
        workspaces = client.compute(graph['workspace'])
        results = client.gather(workspaces)

        print("Appending results to files and removing splits.......")
        graph['rm_splits'].compute()
        write_summary(graph['summary'].compute(), albacore.save_path.joinpath('sequencing_summary.txt'))
        write_data(graph['telemetry'].compute(), albacore.save_path.joinpath('sequencing_telemetry.js'))
        write_config(graph['config'].compute(), albacore.save_path.joinpath('configuration.cfg'))
        write_data(graph['pipe'].compute(), albacore.save_path.joinpath('pipeline.log'))

        batch_chunk_counter += 1
    print("Writing Final results to files....")

    return results

def get_graph(save_path, func, build_command, input_path, batch_splits, batches, barcoding, output_format):
    commands = []
    basecalls = []
    rm_splits = []
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
            copy_files = copy_splits(spl_data[split], this_split_path, None)

            command = get_command(split, batch.name, build_command, input_path, copy_files)
            commands.append(command)

            bc = basecall(func, command)
            basecalls.append(bc)

            split_save_path = save_path.joinpath(batch.name)

            configuration = digest_configuration(split_save_path.joinpath(str(split), 'configuration.cfg'), split_save_path.joinpath('configuration.cfg'), bc)
            if output_format == 'fast5':
                workspace = digest_fast5_workspace(save_path.joinpath(batch.name, str(split), 'workspace'), save_path.joinpath('workspace'), barcoding, bc)
            elif output_format == 'fastq':
                workspace = digest_fastq_workspace(save_path.joinpath(batch.name, str(split), 'workspace'), save_path.joinpath('workspace'), barcoding, bc)

            split_configs.append(configuration)
            split_workspaces.append(workspace)
            split_summaries.append(split_save_path.joinpath(str(split), 'sequencing_summary.txt'))
            split_telemetries.append(split_save_path.joinpath(str(split), 'sequencing_telemetry.js'))
            split_pipelines.append(split_save_path.joinpath(str(split), 'pipeline.log'))

        rm_splits.append(remove_splits(split_path, workspace))
        batch_summaries.extend(split_summaries)
        batch_pipelines.extend(split_pipelines)
        batch_telemetries.extend(split_telemetries)
        batch_configs.extend(split_configs)
        batch_workspaces.extend(split_workspaces)

    digest_rm_splits = digest_splits(rm_splits)
    digested_workspaces = digest_all_workspaces(batch_workspaces)
    bag_summaries = db.read_text(batch_summaries)
    bag_pipelines = db.read_text(batch_pipelines)
    bag_telemetries = db.read_text(batch_telemetries)
    digested_configs = digest_all_configurations(batch_configs)#db.read_text(batch_configs)

    results = sum_results(summ=bag_summaries,
                          tel=bag_telemetries,
                          pipe=bag_pipelines,
                          conf=digested_configs,
                          wrkspc=digested_workspaces,
                          rm_splits=digest_rm_splits)
    return results

if __name__ == '__main__':
    batch_chunk_counter = 3
    batch_bunch_size = 5
    bunches_name = "Processing Batches " + str((1 + batch_chunk_counter * batch_bunch_size)) + "-" + str((batch_chunk_counter + 1) * batch_bunch_size)
    print(bunches_name)
