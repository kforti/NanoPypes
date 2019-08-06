import os
import shutil
from pathlib import Path
import math

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs

from nanopypes.tasks.partition_file_data import BatchPartition

class DataPartitioner:

    def __init__(self, num_batches, save_path, data_type, partitions, partition_strategy, **task_kwargs):
        self.data_type = data_type
        self.save_path = save_path
        self.partitions = partitions
        self.split_merge = partition_strategy
        self.num_batches = num_batches

        self.partition_tasks = []

        self.data_handler = {'ont_sequence': {'one_to_many': partition_ont_seq_data},
                             'ont_basecalled': {'many_to_one': merge_basecalled_data,
                                                'one_to_one': partition_basecalled_data},
                             'ont_demultiplexed': {'merge_by_barcode': partition_demultiplexed_data,
                                                   'many_to_one': None},
                             'mapped_reads': {'merge_by_name': merge_bams,
                                              'one_to_one': sam_to_bam}
                             }
        self.kwargs_handler = {'ont_sequence': {'one_to_many': {'partitions': self.partitions, 'save_path': self.save_path},
                                         'many_to_one': {}},
                               'ont_basecalled': {'many_to_one': {},
                                                  'one_to_one': {'save_path': self.save_path, 'strategy': self.split_merge, 'input_type': 'fastq'}},
                               'mapped_reads': {'merge_by_name': {'save_path': self.save_path},
                                              'one_to_one': {}},
                               'fastq': {'one_to_one': {}},
                               'ont_demultiplexed': {'merge_by_barcode': {'save_path': self.save_path},
                                             'many_to_one': None}
                               }

    def partition_data(self):
        print('data_type', self.data_type)
        print('split_merge', self.split_merge)
        fn = self.data_handler[self.data_type][self.split_merge]
        fn_kwargs = self.kwargs_handler[self.data_type][self.split_merge]

        for i in range(self.num_batches):
            #fn_kwargs['batch_num'] = i
            partition_task = BatchPartition(input_fn=fn, batch_num=i, fn_kwargs=fn_kwargs)
            self.partition_tasks.append(partition_task)

        return self.partition_tasks
        # for i, batch in enumerate(self.inputs):
        #     fn_kwargs['batch_num'] = counter
        #     counter += 1
        #     print(fn_kwargs)
        #     if self.data_type == 'ont_sequence':
        #         partition_task = BatchPartition(batch, fn, fn_kwargs, self.dependencies, name=str(counter))
        #     elif self.data_type == 'ont_mapped_reads':
        #         partition_task = BatchPartition(batch, fn, fn_kwargs, self.dependencies)
        #     else:
        #         partition_task = BatchPartition(batch, fn, fn_kwargs, self.dependencies)

            # with self.pipeline as flow:
            #     results = partition_task()
            #     results.set_upstream(self.dependencies, flow=flow)




#############################################################
### ONT Sequence Functions                                ###
#############################################################

def partition_ont_seq_data(directory, batch_num, partitions, save_path, **kwargs):
    """
    Function for splitting data one to many- meaning that batches are created within the function call.
    :param directory: The directory contained within the nanopypes batch
    :param partitions: The number of partitions the data should be split into
    :param save_path: The location of the save directories
    :return: a tuple containing alist of the batches' command_data, a list of input batches and a list of save batches
    """
    structure, children = get_structure(directory)
    batch_size = math.ceil(len(children) / partitions)
    batches = [children[i:i + batch_size] for i in range(0, len(children), batch_size)]
    if structure == 'dir_dirs':
        results = get_dir_batches(batches, save_path)
    elif structure == 'dir_files':
        results = get_file_batches(batches, directory)

    return results


def get_structure(path):
    """

    :param path:
    :return:
    """
    children = [os.path.join(path, child) for child in os.listdir(path)]
    files = False
    dirs = False
    structure = None
    for child in children:
        if os.path.isfile(child):
            files = True
        elif os.path.isdir(child):
            dirs = True

    if files and dirs:
        structure = 'mix'
    elif files:
        structure = 'dir_files'
    elif dirs:
        structure = 'dir_dirs'

    return structure, children


def get_file_batches(batches, parent_directory, save_path):
    all_results = []
    for i in range(len(batches)):
        batch_name = "batch_{}".format(str(i))
        input_batch_path = os.path.join(parent_directory).joinpath(batch_name)

        os.mkdir(input_batch_path)
        for file in batches[i]:
            shutil.move(file, str(input_batch_path))
        all_results.append({'input': input_batch_path, 'save': os.path.join(save_path, batch_name)})

    return all_results


def get_dir_batches(batches, save_path):
    save_batch_paths = []
    commands = []
    for batch in batches:
        batch_commands = []
        batch_saves = []
        for directory in batch:
            dir_save_path = os.path.join(save_path, os.path.basename(directory))
            batch_saves.append(dir_save_path)
            batch_commands.append({'input': directory, 'save': dir_save_path})
        save_batch_paths.append(batch_saves)
        commands.append(batch_commands)
    #print("SAVES: ", save_batch_paths)

    return commands, batches, save_batch_paths


#############################################################
### ONT Basecalled Functions                              ###
#############################################################

def partition_basecalled_data(batch, batch_num, save_path, strategy='one_to_one', input_type='fastq'):
    if strategy == 'one_to_one':
        if input_type == 'fastq':
            results = _get_fastqs(batch, batch_num, save_path)
        elif input_type == 'main_dir':
            results = _get_main_dirs(batch, save_path)
        #print(results)
    return results

def _get_fastqs(batch, batch_num, save_path, as_string=True):

        batch_command_data = []
        save_paths = []
        batch_path = os.path.join(save_path, "nanopypes_batch_{}".format(str(batch_num)))
        if os.path.exists(batch_path) is False:
            os.mkdir(batch_path)
        for i, directory in enumerate(batch):
            pass_path = os.path.join(directory, "workspace", "pass")
            if as_string:
                fastqs = ""
            elif as_string is False:
                fastqs = []
            save_path = os.path.join(batch_path, "ont_batch_{}.sam".format(os.path.basename(directory)))

            # print("PASS PATH: ", pass_path)
            for fastq in os.listdir(pass_path):
                if as_string:
                    fastqs += (os.path.join(pass_path, fastq) + " ")
                elif as_string is False:
                    fastqs.append((os.path.join(pass_path, fastq) + " "))

            result = {'input': fastqs, 'save': save_path}
            save_paths.append(save_path)
            batch_command_data.append(result)

        # print("fastqs: ", all_fastqs)
        # print("saves: ", save_paths)
        return batch_command_data, batch, save_paths


def _get_main_dirs(batch, save_path):
    input_paths = batch
    save_paths = []
    command_data = []
    for directory in batch:
        dir_name = "batch_{}".format(os.path.basename(directory))
        dir_save_path = os.path.join(save_path, dir_name)
        save_paths.append(dir_save_path)
        command_data.append({'input': directory, 'save': dir_save_path})
    return command_data, input_paths, save_paths


def merge_basecalled_data(save_path):

    import re

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

    for batch in batches:
        if re.match(batch_pattern, batch) == None:
            continue
        shutil.rmtree(str(save_path.joinpath(batch)))


def collapse_config(config_paths, save_path):
    import numpy as np
    from collections import deque
    config_data = {}
    for config in config_paths:
        row_counter = 0
        with open(str(config), "r") as file:
            for row in file:
                if row == '\n':
                    continue
                if (row, row_counter) in config_data:
                    config_data[(row, row_counter)] += 1

                else:
                    config_data[(row, row_counter)] = 1
                row_counter += 1
                # elif row in config_data and i not in write_rows:
                #     write_rows[i] = [row]
                # else:
                #     config_data[row] = [i]
                #     write_rows[i] = [row]
        file.close()
    print(config_data)
    num_configs = int(len(config_paths) * .90)
    data = {}
    unsure = []

    for d in config_data.keys():
        if config_data[d] >= num_configs:
            data[d[1]] = d[0]
        else:
            unsure.append(d[0])
    print(data)
    with open(str(save_path), 'a') as outfile:
        for i in range(len(config_data)):
            try:
                outfile.write(data[i])
            except:
                pass
        if len(unsure) > 0:
            outfile.write(
                "\n\n##################################\nDiscrepencies in configs\n##################################\n")
            outfile.writelines(unsure)

    return


def collapse_seq_summary(sum_paths, save_path):
    header = None
    with open(str(save_path), 'a') as sum_file:
        for ss in sum_paths:
            with open(ss, "r") as file:
                if header is None:
                    sum_file.writelines(file)
                    header = True
                else:
                    for i, row in enumerate(file):
                        if i == 0:
                            continue
                        else:
                            sum_file.write(row)

            file.close()
    sum_file.close()
    return


def collapse_seq_telemetry(tel_paths, save_path):
    with open(str(save_path), 'a') as tel_file:
        for tel in tel_paths:
            with open(tel, 'r') as infile:
                tel_file.writelines(infile)
    tel_file.close()
    return


def collapse_pipeline(pipe_paths, save_path):
    with open(str(save_path), 'a') as pipe_file:
        for pipe in pipe_paths:
            with open(pipe, 'r') as infile:
                pipe_file.writelines(infile)
    pipe_file.close()
    return


def collapse_workspace(workspace_paths, save_path):
    counter = 0
    for workspace in workspace_paths:
        for r, d, f in os.walk(str(workspace)):
            dest_root = r.replace(str(workspace), str(save_path))
            for file in f:
                file_name = str(counter) + "_" + file
                src = Path(r).joinpath(file)
                dest = Path(dest_root).joinpath(file_name)
                shutil.move(str(src), str(dest))
                counter += 1


def prep_save_location(save_path):
    save_path = Path(save_path)
    if save_path.joinpath("workspace").exists() is False:
        save_path.joinpath("workspace").mkdir()
    if save_path.joinpath("workspace", "fail").exists() is False:
        save_path.joinpath("workspace", "fail").mkdir()
    if save_path.joinpath("workspace", "pass").exists() is False:
        save_path.joinpath("workspace", "pass").mkdir()
    if save_path.joinpath("workspace", "calibration_strands").exists() is False:
        save_path.joinpath("workspace", "calibration_strands").mkdir()


#############################################################
### ONT Demultiplexed Functions                                   ###
#############################################################

def partition_demultiplexed_data(batch, batch_num, save_path):
    barcodes = _get_barcodes(batch)
    command_data = []
    batch_inputs = batch
    batch_saves = []

    batch_name = "batch_{}".format(str(batch_num))
    batch_save_path = os.path.join(save_path, batch_name)
    if os.path.exists(batch_save_path) is False:
        os.mkdir(batch_save_path)
    for bcode, paths in barcodes.items():
        fastqs = ""
        for p in paths:
            fastqs += (p + " ")
        save_file = os.path.join(batch_save_path, (bcode + ".sam"))
        command_data.append({'input': fastqs, 'save': save_file})
        batch_saves.append(save_file)
    return command_data, batch_inputs, batch_saves


def _get_barcodes(batch):
    barcodes = {}
    for directory in batch:
        for file in os.listdir(directory):
            barcode = file.replace('.fq', '')
            barcode = file.replace('.fastq', '')
            input_path = os.path.join(directory, file)
            #save_path = os.path.join(self._save_path, file)
            if barcode in barcodes:
                barcodes[barcode].append(input_path)
            elif barcode not in barcodes:
                barcodes[barcode] = [input_path]
    return barcodes


def merge_demultiplexed_data(batches, save_path):
    barcodes = {}
    for batch in batches:
        batch_barcodes = _get_barcodes(batch)
        for bcode, paths in batch_barcodes.items():
            if bcode in barcodes:
                barcodes[bcode].extend(paths)
            else:
                barcodes[bcode] = paths

    for bcode, paths in barcodes.items():
        bcode_save_path = os.path.join(save_path, bcode)
        if os.path.exists(bcode_save_path) is False:
            os.mkdir(bcode_save_path)
        for i, file in enumerate(paths):
            file_name = "{}_{}".format(str(i), os.path.basename(file))
            file_save_path = os.path.join(bcode_save_path, file_name)
            shutil.move(file, file_save_path)


def merge_mapped_reads(batches, save_path):
    for batch in batches:
        for i, file in enumerate(batch):
            file_name = "{}_{}". format(str(i), os.path.basename(file))
            file_save_path = os.path.join(save_path, file_name)
            shutil.move(file, file_save_path)


#############################################################
### Mapped Reads Functions                                ###
#############################################################

def sam_to_bam(batch, batch_num, **fn_kwargs):
    command_data = []
    input_paths = batch
    save_paths = []
    for file in batch:
        path = Path(file)
        bam_name = path.name.replace(".sam", ".bam")
        bam_path = str(path.parent.joinpath(bam_name))
        save_paths.append(bam_path)
        command_data.append({'input': file, 'save': bam_path})
    return command_data, input_paths, save_paths

def merge_bams(batches, batch_num, save_path):
    save_path = os.path.join(save_path, 'merged_bams')
    if os.path.exists(save_path) is False:
        os.mkdir(save_path)

    barcodes = _find_barcodes(batches)
    batch_inputs = []
    batch_saves = []
    batch_command_data = []

    for bcode, paths in barcodes.items():
        print("PATHS: ", paths)
        bcode_inputs = " ".join(paths)
        batch_inputs.append(bcode_inputs)
        bcode_save_path = os.path.join(save_path, bcode)
        batch_saves.append(bcode_save_path)
        batch_command_data.append({'input': bcode_inputs, 'save': bcode_save_path})

    command_data = list(batch_command_data)
    input_paths = list(batch_inputs)
    save_paths = list(batch_saves)

    return command_data, input_paths, save_paths



def _find_barcodes(batches):
    bam_barcodes = {}
    for batch in batches:
        for file in batch:
            file_name = os.path.basename(file)
            if file_name in bam_barcodes:
                bam_barcodes[file_name].append(file)
            else:
                bam_barcodes[file_name] = [file]
    return bam_barcodes


class FileData():

    def __init__(self, save_path, dependencies,
                 inputs=None, demultiplex=False, merge=False, partitions=None, **kwargs):
        #super().__init__(**kwargs)
        self.inputs = inputs
        self.save_path = save_path
        self.partitions = partitions
        self.dependencies = dependencies
        self.merge = merge
        self.demultiplex = demultiplex
        #self.multi_fast5 = self._is_multi_fast5()

        self._structure_modified = False
        #self._get_structure()

    @property
    def num_batches(self):
        return self.partitons

    @property
    def num_children(self):
        return len(self._children)

    def get_structure(self, path):
        children = [os.path.join(path, child) for child in os.listdir(path)]
        files = False
        dirs = False
        structure = None
        for child in children:
            if os.path.isfile(child):
                files = True
            elif os.path.isdir(child):
                dirs = True

        if files and dirs:
            structure = 'mix'
        elif files:
            structure = 'dir_files'
        elif dirs:
            structure = 'dir_dirs'

        return structure, children

    def get_batches(self):
        pass


class ONTDemultiplexedData(FileData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.input = self._input_paths
        self.barcodes = {}

    def run(self):
        self._find_barcodes()
        results = self._get_paths()

        #return {'input': input_batches, 'save': save_batches}

        return results

    def _find_barcodes(self):
        for batch in self.inputs:
            for directory in batch:
                for file in os.listdir(directory):
                    barcode = file.replace('.fq', '')
                    barcode = file.replace('.fastq', '')
                    input_path = os.path.join(directory, file)
                    save_path = os.path.join(self._save_path, file)
                    if barcode in self.barcodes:
                        self.barcodes[barcode].append(input_path)
                    elif barcode not in self.barcodes:
                        self.barcodes[barcode] = [input_path]

    def _get_paths(self):
        all_results = []
        for barcode, paths in self.barcodes.items():
            if self.merge is False:
                input_fastqs = ""
                for path in paths:
                    input_fastqs += (path + " ")
                all_results.append({'input': input_fastqs, 'save': os.path.join(self._save_path, (barcode + ".sam"))})
            elif self.merge:
                barcode_save = os.path.join(self._save_path, barcode)
                os.mkdir(barcode_save)
                for path in paths:
                    save_path = os.path.join(barcode_save, os.path.basename(path))
                    shutil.move(path, save_path)
        return all_results


class ONTFastqSequenceData(FileData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @defaults_from_attrs("inputs")
    def run(self, inputs=None):
        all_commands, all_inputs, all_saves = [], [], []
        for i, batch in enumerate(inputs):
            if self.demultiplex is False:
                commands, inputs, saves = self._get_fastqs(batch, i)#self.inputs[i])
            elif self.demultiplex:
                result = self._get_demultiplex_paths(batch)#self.inputs[i])
            all_commands.append(commands)
            all_inputs.append(inputs)
            all_saves.append(saves)
        print("FASTQ INPUTS: ", all_inputs)
        print("FASTQ SAVES: ", all_saves)
        return all_commands, all_inputs, all_saves

    def _get_fastqs(self, batch, batch_num):
        batch_command_data = []
        save_paths = []
        batch_path = os.path.join(self.save_path, "nanopypes_batch_{}".format(str(batch_num)))
        if os.path.exists(batch_path) is False:
            os.mkdir(batch_path)
        for i, directory in enumerate(batch):
            pass_path = os.path.join(directory, "workspace", "pass")
            fastqs = ""
            save_path = os.path.join(batch_path, "ont_batch_{}".format(os.path.basename(directory)))
            if os.path.exists(save_path) is False:
                os.mkdir(save_path)
            #print("PASS PATH: ", pass_path)
            for fastq in os.listdir(pass_path):
                fastqs += (os.path.join(pass_path, fastq) + " ")

            result = {'input': fastqs, 'save': save_path}
            save_paths.append(save_path)
            batch_command_data.append(result)

        #print("fastqs: ", all_fastqs)
        #print("saves: ", save_paths)
        return batch_command_data, batch, save_paths

    def _get_demultiplex_paths(self, batch):
        save_paths = []
        for directory in batch:
            save_paths.append(os.path.join(self.save_path, os.path.basename(directory)))

        return batch, save_paths


class ONTSequenceData(FileData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, inputs=None):
        structure, children = self.get_structure(inputs[0])
        batch_size = math.ceil(len(children) / self.partitions)
        batches = [children[i:i + batch_size] for i in range(0, len(children), batch_size)]
        if structure == 'dir_dirs':
            results = self._get_dir_batches(batches)
        elif structure == 'dir_files':
            results = self._get_file_batches(batches)

        return results

    def _get_dir_batches(self, batches):
        save_batch_paths = []
        commands = []
        for batch in batches:
            batch_commands = []
            batch_saves = []
            for directory in batch:
                save_path = os.path.join(self.save_path, os.path.basename(directory))
                batch_saves.append(save_path)
                batch_commands.append({'input': directory, 'save': save_path})
            save_batch_paths.append(batch_saves)
            commands.append(batch_commands)
        print("SAVES: ", save_batch_paths)

        return commands, batches, save_batch_paths

    def _get_file_batches(self, batches):
        # input_batch_paths = []
        # save_batch_paths = []
        all_results = []
        for i in range(len(batches)):
            batch_name = "batch_{}".format(str(i))
            input_batch_path = os.path.join(self.parent_directory).joinpath(batch_name)
            #input_batch_paths.append(input_batch_path)
            os.mkdir(input_batch_path)
            for file in batches[i]:
                shutil.move(file, str(input_batch_path))
            all_results.append({'input': input_batch_path, 'save': os.path.join(self.save_path, batch_name)})
            #save_batch_paths.append(Path(self._save_path).joinpath(batch_name))
        self._structure_modified = True
        #return input_batch_paths, save_batch_paths
        return all_results


# if __name__ == '__main__':
#     from prefect import Flow
#
#     from nanopypes.distributed_data.pipeline_data import get_commands
#     from nanopypes.pipes.base2 import PrintCommands
#
#     flow = Flow('test-flow')
#     inputs = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"]
#     template = "read_fast5_basecaller.py --input {input} --save_path {save} --flowcell yesflow --kit thiskit --output_format fastq --worker_threads 1 --reads_per_fastq 1000"
#     template2 = "minimap2 -ax splice /path/to/reference {input} -o {save}"
#     data = ONTSequenceData(inputs=inputs,
#                            save_path="/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy",
#                            dependencies=None,
#                            partitions=4,
#                            name='test-task')
#     data = ONTFastqSequenceData(inputs=data[2],
#                                 save_path="some/save/path/",
#                                 dependencies=[],
#                                 partitions=4,
#                                 name='task_test',
#                                 )
#     cmds = PrintCommands()
#     with flow as f:
#         results = data()
#
#         commands = get_commands(results[0], template)
#         cmds(commands)
#
#     flow.run()
#
#     print(results)
#

if __name__ == '__main__':
    batches = [['/nl/umw_athma_pai/kevin/test_ercc/map/batch_1/BC01.bam', '/nl/umw_athma_pai/kevin/test_ercc/map/batch_1/BC04.bam', '/nl/umw_athma_pai/kevin/test_ercc/map/batch_1/BC02.bam', '/nl/umw_athma_pai/kevin/test_ercc/map/batch_1/BC03.bam', '/nl/umw_athma_pai/kevin/test_ercc/map/batch_1/none.bam'],
               ['/nl/umw_athma_pai/kevin/test_ercc/map/batch_0/BC01.bam',
                '/nl/umw_athma_pai/kevin/test_ercc/map/batch_0/BC04.bam',
                '/nl/umw_athma_pai/kevin/test_ercc/map/batch_0/BC02.bam',
                '/nl/umw_athma_pai/kevin/test_ercc/map/batch_0/BC03.bam',
                '/nl/umw_athma_pai/kevin/test_ercc/map/batch_0/none.bam']]
    save_path = '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests'

    data = merge_bams(batches, 0, save_path)
    print(data)






