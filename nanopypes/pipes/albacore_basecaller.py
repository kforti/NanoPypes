from pathlib import Path
from copy import copy
import os
import shutil
import re

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

        # print("testing user input")
        #
        # try:
        #     user_input = with_timeout(timeout=20, future=self.control_client())
        #     print(user_input)
        # except TimeoutError:
        #     print("Timeout")



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

            for key in graph.keys():
                graph[key].visualize()

            print("Computing the Graph ")
            basecalls = self.client.compute(graph['basecall'])
            # print("you can control the client....\n Enter Commands:")
            # while basecalls.done() != True:
            #     input()
            #     self.client.
            basecall_results = self.client.gather(basecalls)

            print("Creating final secondary output files.......")
            write_summary(graph['summary'].compute(), self.save_path.joinpath('sequencing_summary.txt'))
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
        batch_basecalls = []

        for batch in batch_bunch:
            self._process_splits(batch)

            batch_summaries.extend(self.split_summaries)
            batch_pipelines.extend(self.split_pipelines)
            batch_telemetries.extend(self.split_telemetries)
            batch_configs.extend(self.split_configs)
            batch_basecalls.extend(self.split_basecalls)

        self.all_basecalls = run_all_basecalls(batch_basecalls)
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
        bc_graph = basecall_graph(workspace, rm_split)
        return bc_graph

    def write_nanopypes_log(self):
        pass

    def control_client(self):
        user_input = input()
        return user_input


@dask.delayed
def rm_batch_results(save_path):
    save_path = copy(save_path)
    batch_pattern = r'(^)[0-9]+($)'
    for child in os.listdir(str(save_path)):
        if re.match(batch_pattern, child):
            shutil.rmtree(str(save_path.joinpath(child)))

@dask.delayed
def rm_split_data_dirs(batches):
    batches = copy(batches)
    for batch in batches:
        try:
            os.rmdir(str(batch.joinpath('split_data')))
        except FileNotFoundError:
            pass

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
def copy_splits(splits, split_path):
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
def remove_splits(split_path, dependencies):
    try:
        split_path = copy(split_path)
        shutil.rmtree(str(split_path))
    except FileNotFoundError as e:
        pass
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
def basecall_graph(workspace, rmsplit):
    return workspace, rmsplit

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
def digest_fastq_workspace(workspace_path, save_path, barcoding, bc):
    for read_type in os.listdir(str(workspace_path)):
        try:
            save_path.joinpath(read_type).mkdir()
        except FileExistsError:
            pass

        if barcoding and read_type != 'calibration_strands':
            for barcode in os.listdir(str(workspace_path.joinpath(read_type))):
                try:
                    save_path.joinpath(read_type, barcode).mkdir()
                except FileExistsError:
                    pass
                for fastq in os.listdir(str(workspace_path.joinpath(read_type, barcode))):
                    fastq_data = []
                    read_finish = False
                    write_finish = False
                    while read_finish == False:
                        try:
                            with open(str(workspace_path.joinpath(read_type, barcode, fastq)), 'r') as split_file:
                                for line in split_file:
                                    fastq_data.append(line)
                            read_finish = True
                            split_file.close()
                        except IOError as e:
                            print('error1', e)
                            pass

                    while write_finish == False:
                        try:
                            with open(str(save_path.joinpath(read_type, barcode, fastq)), 'a') as final_file:
                                for line in fastq_data:
                                    final_file.write(line)
                            write_finish = True
                            final_file.close()
                            os.remove(str(workspace_path.joinpath(read_type, barcode, fastq)))
                        except IOError as e:
                            print('error2', e)
                            pass

        elif barcoding == False or read_type == 'calibration_strands':
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
    return basecalls

@dask.delayed
def digest_all_fast5_workspaces(workspace):
    return workspace

@dask.delayed
def digest_all_fastq_workspaces(workspace, barcoding):
    cal_fastqs = db.read_text(workspace['cailbration_strands'])
    if barcoding:
        pass_fastqs = {}
        fail_fastqs = {}
        for barcode in workspace['pass'].keys():
            pass_fastqs[barcode] = db.read_text(workspace['pass'][barcode])
        for barcode in workspace['fail'].keys():
            fail_fastqs[barcode] = db.read_text(workspace['fail'][barcode])

        bag_workpsace = {'calibration_strands': [],
           'pass': {},
           'fail': {}}
    elif barcoding == False:
        pass_fastqs = db.read_text(workspace['pass'])
        fail_fastqs = db.read_text(workspace['fail'])


    bag_workspace = {'calibration_strands': cal_fastqs,
                     'pass': pass_fastqs,
                     'fail': fail_fastqs}

    return bag_workspace

@dask.delayed
def digest_all_configurations(configs):
    return configs

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
    if output_format == 'fastq' and barcoding:
        workspace_dict = {'calibration_strands': [],
                          'pass': {},
                          'fail': {}}
    elif output_format == 'fastq':
        workspace_dict = {'calibration_strands': [],
                          'pass': [],
                          'fail': []}

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
                workspace_dict = digest_fastq_workspace(workspace_path=save_path.joinpath(batch.name, str(split), 'workspace'),
                                                        workspace_dict=workspace_dict,
                                                        barcoding=barcoding,
                                                        bc=bc)

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

    if output_format == 'fast5':
        digested_workspaces = digest_all_fast5_workspaces(batch_workspaces)
    elif output_format == 'fastq':
        digested_workspaces = digest_all_fast5_workspaces(workspace_dict)


    digest_rm_splits = digest_splits(rm_splits)
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





if __name__ == '__main__':
    workspace_dict = {'pass': {'01': 'myfastq.file'}}

    read_type = 'pass'
    barcode = '02'
    try:
        workspace_dict[read_type][barcode]
        print('there')
    except KeyError:
        workspace_dict[read_type][barcode] = []
        print('not there')
