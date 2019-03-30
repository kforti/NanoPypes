from pathlib import Path
import os
import shutil
import re
import sys
import time

import dask
import dask.bag as db
from dask.distributed import wait

from tornado.gen import with_timeout
from tornado.util import TimeoutError

from nanopypes.pipes.base import Pipe


class AlbacoreBasecaller(Pipe):

    def __init__(self, client, albacore, num_splits, batch_bunch_size):
        print("Starting the parallel Albacore Basecaller...")
        self.client = client
        self.num_splits = num_splits
        self.batch_bunch_size = batch_bunch_size
        self.albacore = albacore
        self.barcoding = albacore.barcoding
        self.output_format = albacore.output_format
        self.function = albacore.build_func()
        self.input_path = Path(albacore.input_path)
        self.save_path = Path(albacore.save_path)
        self.all_batches = albacore.batches
        self.batch_bunches = batch_generator(self.all_batches, batch_bunch_size)

        self.all_basecalls = []

    def _prep_save_path(self):
        if self.save_path.joinpath('sequencing_telemetry.js').exists() == False:
            self.save_path.joinpath('sequencing_telemetry.js').touch()
        if self.save_path.joinpath('sequencing_summary.txt').exists() == False:
            self.save_path.joinpath('sequencing_summary.txt').touch()
        if self.save_path.joinpath('pipeline.log').exists() == False:
            self.save_path.joinpath('pipeline.log').touch()
        if self.save_path.joinpath('configuration.cfg').exists() == False:
            self.save_path.joinpath('configuration.cfg').touch()
        if self.save_path.joinpath('workspace').exists() == False:
            self.save_path.joinpath('workspace').mkdir()
        return

    def execute(self):
        self._prep_save_path()

        batch_chunk_counter = 0
        for batch_bunch in self.batch_bunches:
            bunches_name = "Processing Batches " + str((1 + batch_chunk_counter * self.batch_bunch_size)) + "-" + str(
                (batch_chunk_counter + 1) * self.batch_bunch_size)
            print(bunches_name)
            print("Creating the Compute Graph ")
            graph = self.build_graphs(batch_bunch)

            # for key in graph.keys():
            #     graph[key].visualize()

            print("Computing the Graph ")
            basecalls = self.client.compute(graph['basecall'])
            print("after compute is caller", sys.getsizeof(basecalls))
            # print("you can control the client....\n Enter Commands:")
         
            basecall_results = self.client.gather(basecalls)
            print("results...", sys.getsizeof(basecall_results))

            print("Creating final secondary output files.......")
            write_summary(self.client.compute(graph['summary']), self.save_path.joinpath('sequencing_summary.txt'))
            write_data(graph['telemetry'].compute(), self.save_path.joinpath('sequencing_telemetry.js'))
            write_config(graph['config'].compute(), self.save_path.joinpath('configuration.cfg'))
            write_data(graph['pipe'].compute(), self.save_path.joinpath('pipeline.log'))
            futures = self.client.compute([rm_batch_results(self.save_path), rm_split_data_dirs(batch_bunch)])
            wait(futures)
            batch_chunk_counter += 1
        print("Writing Final results to files....")

        return

    def build_graphs(self, batch_bunch):#, save_path, func, build_command, input_path, batch_splits, batches, barcoding, output_format):
        batch_telemetries = []
        batch_summaries = []
        batch_pipelines = []
        batch_configs = []

        for batch in batch_bunch:
            self._process_splits(batch)

            batch_summaries.extend(self.split_summaries)
            batch_pipelines.extend(self.split_pipelines)
            batch_telemetries.extend(self.split_telemetries)
            batch_configs.extend(self.split_configs)
            self.all_basecalls.extend(self.split_basecalls)

        self.bag_summaries = db.read_text(batch_summaries)
        self.bag_pipelines = db.read_text(batch_pipelines)
        self.bag_telemetries = db.read_text(batch_telemetries)
        self.digested_configs = digest_all_configurations(batch_configs)  # db.read_text(batch_configs)

        return self.sum_results()

    def sum_results(self):
        results = {'telemetry': self.bag_telemetries,
                   'summary': self.bag_summaries,
                   'config': self.digested_configs,
                   'pipe': self.bag_pipelines,
                   'basecall': self.all_basecalls}
        return results

    def _process_splits(self, batch):
        #Set split_data path and create directory if it does not exist
        split_path = self.input_path.joinpath(batch.name, 'split_data')
        if split_path.exists() == False:
            try:
                split_path.mkdir()
            except Exception as e:
                raise IOError("There is already a split_data directory in the ", batch.name, " directory")

        chunk_size = int((len(os.listdir(str(batch))) / self.num_splits))
        basecall_graphs = []
        self.split_summaries = []
        self.split_pipelines = []
        self.split_telemetries = []
        self.split_configs = []
        self.split_basecalls = []

        # create split data graph

        spl_data = get_split_paths(batch, chunk_size)

        for split in range(self.num_splits):
            this_split_path = split_path.joinpath(str(split))
            split_save_path = self.save_path.joinpath(batch.name)
            if this_split_path.exists() == False:
                try:
                    this_split_path.mkdir()
                except Exception as e:
                    pass

            split_paths = spl_data[split]
            bc_graph = self._basecall_graph(split=split,
                                            batch=batch,
                                            split_path=this_split_path,
                                            split_paths=split_paths)
            basecall_graphs.append(bc_graph)

            #create config digest graph
            configuration = digest_configuration(split_save_path.joinpath(str(split), 'configuration.cfg'),
                                                 split_save_path.joinpath('configuration.cfg'), bc_graph)
            self.split_configs.append(configuration)
            self.split_basecalls.append(bc_graph)
            self.split_summaries.append(split_save_path.joinpath(str(split), 'sequencing_summary.txt'))
            self.split_telemetries.append(split_save_path.joinpath(str(split), 'sequencing_telemetry.js'))
            self.split_pipelines.append(split_save_path.joinpath(str(split), 'pipeline.log'))

        return

    def _basecall_graph(self, split, batch, split_path, split_paths):
        # create copy data graph
        copy_files = copy_splits(split_paths, split_path)
        command = get_command(split, batch.name, self.albacore.build_command, self.input_path, copy_files)
        bc = basecall(self.function, command)
        rm_split = remove_splits(split_path, bc)

        if self.output_format == 'fast5':
            workspace = digest_fast5_workspace(self.save_path.joinpath(batch.name, str(split), 'workspace'),
                                               self.save_path.joinpath('workspace'), self.barcoding, bc)
        elif self.output_format == 'fastq':
            workspace = digest_fastq_workspace(
                workspace_path=self.save_path.joinpath(batch.name, str(split), 'workspace'),
                save_path=self.save_path.joinpath('workspace'),
                barcoding=self.barcoding,
                bc=bc)

        return basecall_graph(workspace, rm_split)

    def write_nanopypes_log(self):
        pass

    def control_client(self):
        user_input = input()
        return user_input

######################################################################################
##### Basecall Graph                                                                ##
######################################################################################

@dask.delayed
def rm_batch_results(save_path):
    #The regex is for matching matching the batch directory names
    for child in os.listdir(str(save_path)):
        if re.match(r'(^)[0-9]+($)', child):
            shutil.rmtree(str(save_path.joinpath(child)))
    return

@dask.delayed
def rm_split_data_dirs(batches):
    for batch in batches:
        try:
            os.rmdir(str(batch.joinpath('split_data')))
        except FileNotFoundError:
            pass
    return

@dask.delayed
def get_split_paths(batch, chunk_size):
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
def copy_splits(splits, split_path):
    for file in splits:
        new_file_path = split_path.joinpath(file.name)
        try:
            shutil.copyfile(str(file), str(new_file_path))
        except Exception as e:
            return (str(file), str(new_file_path))

    return

@dask.delayed
def remove_splits(split_path, dependencies):
    try:
        shutil.rmtree(str(split_path))
    except FileNotFoundError as e:
        pass
    return

@dask.delayed
def digest_splits(rm_splits):
    return

@dask.delayed
def get_command(split, batch_name, build_command, input_path, splt_data):
    command = build_command(str(input_path.joinpath(batch_name, 'split_data', str(split))), batch_name)
    return command

@dask.delayed
def basecall(func, command):
    return func(command)

@dask.delayed
def basecall_graph(workspace, rmsplit):
    return

@dask.delayed
def digest_configuration(path, save_path, bc):
    data = []
    with open(str(path), 'r') as infile:
        for line in infile:
            data.append(line)
    infile.close()
    return data

@dask.delayed
def digest_fast5_workspace(path, save_path, barcoding, bc):
    for read_type in os.listdir(str(path)):
        if save_path.joinpath(read_type).exists() == False:
            try:
                save_path.joinpath(read_type).mkdir()
            except FileExistsError:
                pass
        #
        # if barcoding and read_type != 'calibration_strands':
        #     for barcode in os.listdir(str(path.joinpath(read_type))):
        #         if save_path.joinpath(read_type, barcode).exists() == False:
        #             try:
        #                 save_path.joinpath(read_type, barcode).mkdir()
        #             except FileExistsError:
        #                 pass
        #         for bcode_batch in os.listdir(str(path.joinpath(read_type, barcode))):
        #             if save_path.joinpath(read_type, barcode, bcode_batch).exists() == False:
        #                 try:
        #                     save_path.joinpath(read_type, barcode, bcode_batch).mkdir()
        #                 except FileExistsError:
        #                     pass
        #             for read in os.listdir(str(path.joinpath(read_type, barcode, bcode_batch))):
        #                 shutil.move(str(path.joinpath(read_type, barcode, bcode_batch, read)),
        #                             str(save_path.joinpath(read_type, barcode, bcode_batch, read)))

        #elif barcoding == False or read_type == 'calibration_strands':
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
def digest_fastq_workspace(workspace_path, save_path, barcoding, bc):
    for read_type in os.listdir(str(workspace_path)):
        try:
            save_path.joinpath(read_type).mkdir()
        except FileExistsError:
            pass
        #
        # if barcoding and read_type != 'calibration_strands':
        #     for barcode in os.listdir(str(workspace_path.joinpath(read_type))):
        #         try:
        #             save_path.joinpath(read_type, barcode).mkdir()
        #         except FileExistsError:
        #             pass
        #         for fastq in os.listdir(str(workspace_path.joinpath(read_type, barcode))):
        #             fastq_data = []
        #             read_finish = False
        #             write_finish = False
        #             while read_finish == False:
        #                 try:
        #                     with open(str(workspace_path.joinpath(read_type, barcode, fastq)), 'r') as split_file:
        #                         for line in split_file:
        #                             fastq_data.append(line)
        #                     read_finish = True
        #                     split_file.close()
        #                 except IOError as e:
        #                     print('error1', e)
        #                     pass
        #
        #             while write_finish == False:
        #                 try:
        #                     with open(str(save_path.joinpath(read_type, barcode, fastq)), 'a') as final_file:
        #                         for line in fastq_data:
        #                             final_file.write(line)
        #                     write_finish = True
        #                     final_file.close()
        #                     os.remove(str(workspace_path.joinpath(read_type, barcode, fastq)))
        #                 except IOError as e:
        #                     print('error2', e)
        #                     pass

        #elif barcoding == False or read_type == 'calibration_strands':
        for fastq in os.listdir(str(workspace_path.joinpath(read_type))):
            fastq_data = []
            read_finish = False
            write_finish = False
            while read_finish == False:
                try:
                    with open(str(workspace_path.joinpath(read_type, fastq)), 'r') as split_file:
                        for line in split_file:
                            fastq_data.append(line)
                    read_finish = True
                    split_file.close()
                except IOError as e:
                    print('error3', e)
                    pass

            while write_finish == False:
                try:
                    with open(str(save_path.joinpath(read_type, fastq)), 'a') as final_file:
                        for line in fastq_data:
                            final_file.write(line)
                    write_finish = True
                    final_file.close()
                    os.remove(str(workspace_path.joinpath(read_type, fastq)))
                except IOError as e:
                    print('error4', e)
                    pass

    return

@dask.delayed
def run_all_basecalls(basecalls):
    return

@dask.delayed
def digest_all_fast5_workspaces(workspace):
    return

@dask.delayed
def digest_all_configurations(configs):
    return configs

def write_data(data, save_path):
    with open(str(save_path), 'a') as file:
        for row in data:
            file.write(row)
    file.close()
    return

def write_config(data, save_path):
    final_config_data = []
    with open(str(save_path), 'r') as file:
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
    with open(str(save_path), 'a') as file:
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

