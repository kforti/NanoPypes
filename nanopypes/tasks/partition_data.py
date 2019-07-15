import os
import shutil
from pathlib import Path
import math

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs


class FileData(Task):

    def __init__(self, save_path, dependencies,
                 inputs=None, demultiplex=False, merge=False, partitions=None, **kwargs):
        super().__init__(**kwargs)
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

    @defaults_from_attrs("inputs")
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


if __name__ == '__main__':
    from prefect import Flow

    from nanopypes.distributed_data.pipeline_data import get_commands
    from nanopypes.pipes.base2 import PrintCommands

    flow = Flow('test-flow')
    inputs = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"]
    template = "read_fast5_basecaller.py --input {input} --save_path {save} --flowcell yesflow --kit thiskit --output_format fastq --worker_threads 1 --reads_per_fastq 1000"
    template2 = "minimap2 -ax splice /path/to/reference {input} -o {save}"
    data = ONTSequenceData(inputs=inputs,
                           save_path="/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy",
                           dependencies=None,
                           partitions=4,
                           name='test-task')
    data = ONTFastqSequenceData(inputs=data[2],
                                save_path="some/save/path/",
                                dependencies=[],
                                partitions=4,
                                name='task_test',
                                )
    cmds = PrintCommands()
    with flow as f:
        results = data()

        commands = get_commands(results[0], template)
        cmds(commands)

    flow.run()

    print(results)


