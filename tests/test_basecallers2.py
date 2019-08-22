from pathlib import Path
import subprocess
import os
import csv
import shutil

from nanopypes.core.basecaller import AlbacoreBasecaller, GuppyBasecaller, collapse_data
from nanopypes import ClusterManager
from config import Configuration
from compute import Cluster

from distributed import LocalCluster, Client


########################################################################
### Test Albacore Local                                              ###
########################################################################

def test_albcore_build_command():
    flowcell = 'FLO-MIN106'
    batches = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    output_format = 'fastq'

    expected_commands = [["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                        "--kit", "SQK-LSK109", "--output_format", "fastq",
                        "--save_path", "test_data/basecalled_data/results/local_basecall_test/0",
                        "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/0',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/1",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/1',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/2",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/2',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/3",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/3',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/4",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/4',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/5",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/5',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/6",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/6',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/7",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/7',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/8",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/8',
                          "--reads_per_fastq_batch", "1000"],
                         ["read_fast5_basecaller.py", "--flowcell", "FLO-MIN106",
                          "--kit", "SQK-LSK109", "--output_format", "fastq",
                          "--save_path", "test_data/basecalled_data/results/local_basecall_test/9",
                          "--worker_threads", "1", "--input", 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/9',
                          "--reads_per_fastq_batch", "1000"]]

    albacore = AlbacoreBasecaller(cluster=None,
                                  input_path="test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/",
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format=output_format,
                                  reads_per_fastq=1000)

    for i in range(len(batches)):
        cmd = albacore.build_basecall_command(batches[i])
        try:
            assert cmd == expected_commands[i]
        except AssertionError:
            print("generated command: ", cmd)
            print("expected command: ", expected_commands[i])
            print()
            raise AssertionError

def test_albacore_batches():
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    flowcell = 'FLO-MIN106'
    input_path  = "test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/"
    expected_batches = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    albacore = AlbacoreBasecaller(cluster=None, input_path=input_path,
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format="",
                                  reads_per_fastq=1000)
    for i, batch in enumerate(albacore.batches()):
        if batch in expected_batches:
            expected_batches.remove(batch)
        else:
            raise AssertionError("Albacore batches broke")
    assert expected_batches == []


def test_albacore_binary():
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    flowcell = 'FLO-MIN106'
    input_path = "test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/"
    expected_stdout = b'usage: read_fast5_basecaller.py [-h] [-l] [-v] [-i INPUT] -t WORKER_THREADS -s\n                                SAVE_PATH [--resume [X]] [-f FLOWCELL]\n                                [-k KIT] [--barcoding] [-c CONFIG]\n                                [-d DATA_PATH] [-b] [-r]\n                                [-n FILES_PER_BATCH_FOLDER] [-o OUTPUT_FORMAT]\n                                [-q READS_PER_FASTQ_BATCH]\n                                [--disable_filtering] [--disable_pings]\n\nONT Albacore Sequencing Pipeline Software\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -l, --list_workflows  List standard flowcell / kit combinations.\n  -v, --version         Print the software version.\n  -i INPUT, --input INPUT\n                        Folder containing read single_read_fast5 files (if not present,\n                        will expect file names on stdin).\n  -t WORKER_THREADS, --worker_threads WORKER_THREADS\n                        Number of worker threads to use.\n  -s SAVE_PATH, --save_path SAVE_PATH\n                        Path to save output.\n  --resume [X]          Resume previous run for the given save path. Optional\n                        parameter X is for debugging purposes only.\n  -f FLOWCELL, --flowcell FLOWCELL\n                        Flowcell used during the sequencing run.\n  -k KIT, --kit KIT     Kit used during the sequencing run.\n  --barcoding           Search for barcodes to demultiplex sequencing data.\n  -c CONFIG, --config CONFIG\n                        Optional configuration file to use.\n  -d DATA_PATH, --data_path DATA_PATH\n                        Optional path to model files.\n  -b, --debug           Output additional debug information to the log.\n  -r, --recursive       Recurse through subfolders for input data files.\n  -n FILES_PER_BATCH_FOLDER, --files_per_batch_folder FILES_PER_BATCH_FOLDER\n                        Maximum number of files in each batch subfolder. Set\n                        to 0 to disable batch subfolders.\n  -o OUTPUT_FORMAT, --output_format OUTPUT_FORMAT\n                        desired output format, can be fastq,single_read_fast5 or only one\n                        of these.\n  -q READS_PER_FASTQ_BATCH, --reads_per_fastq_batch READS_PER_FASTQ_BATCH\n                        number of reads per FastQ batch file. Set to 1 to\n                        receive one reads per file and file names which\n                        include the read ID. Set to 0 to have all reads per\n                        run ID written to one file.\n  --disable_filtering   Disable filtering into pass/fail folders\n  --disable_pings       Do not send summary information about the run\n'

    albacore = AlbacoreBasecaller(client=None, expected_workers=None, input_path=input_path,
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format="",
                                  reads_per_fastq=1000)
    func = albacore.command_function(stdout=subprocess.PIPE)
    comp_process = func(["read_fast5_basecaller.py", "--help"])
    assert comp_process.stdout == expected_stdout


def test_albacore_basecall():
    save_path = Path('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_test')
    if save_path.exists():
        shutil.rmtree(str(save_path))
    save_path.mkdir()

    flowcell = 'FLO-MIN106'
    input_path = Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass')
    kit = 'SQK-LSK109'
    output_format = 'fastq'
    cluster = ClusterManager(cluster=LocalCluster())

    albacore = AlbacoreBasecaller(cluster=cluster, input_path=input_path,
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format=output_format,
                                  reads_per_fastq=1000)
    albacore()

    collapsed_reads = {}
    for dir_name, subdirs, files in os.walk(str(save_path.joinpath("workspace"))):
        if Path(dir_name).parent.name == "workspace":
            collapsed_reads[Path(dir_name).name] = {}
        for file in files:
            if ".fastq" in Path(file).suffixes:
                fq = str(Path(dir_name).joinpath(file))
                with open(fq, 'r') as file:
                    for read in fastq_read_generator(file):
                        read_name = read["header"].split()[0][1:]
                        read_len = len(read["sequence"])
                        collapsed_reads[Path(dir_name).name][(read_name, read_len)] = 0
    # print(collapsed_reads)
    for batch in os.listdir(str(input_path)):
        for file in os.listdir(str(input_path.joinpath(batch))):
            if ".fastq" in Path(file).suffixes:
                fq = str(input_path.joinpath(batch, file))
                with open(fq, 'r') as f:
                    for read in fastq_read_generator(f):
                        read_name = read["header"].split()[0][1:]
                        read_len = len(read["sequence"])
                        assert collapsed_reads[batch][(read_name, read_len)] == 0
                        collapsed_reads[batch][(read_name, read_len)] = 1

    for key in collapsed_reads:
        for key, value in collapsed_reads[key].items():
            assert value == 1
    # input_reads = {}
    # for batch in os.listdir(str(input_path)):
    #
    #     if batch[0] == ".":
    #         continue
    #     for read in os.listdir(str(input_path.joinpath(batch))):
    #         input_reads[read] = 0
    #
    # seq_sum = str(save_path.joinpath("sequencing_summary.txt"))
    # with open(seq_sum, 'r') as f:
    #     seq_sum_data = {}
    #     csv_reader = csv.reader(f, delimiter="\t")
    #     for i, row in enumerate(csv_reader):
    #         # print(row)
    #         seq_sum_data[row[1]] = row[0]
    #
    # f.close()
    #
    # for dir_name, subdirs, files in os.walk(str(save_path.joinpath("workspace"))):
    #     # print(dir_name)
    #     for file in files:
    #         # print(file)
    #         if ".fastq" in Path(file).suffixes:
    #             fq = str(Path(dir_name).joinpath(file))
    #             with open(fq, 'r') as file:
    #                 for read in fastq_read_generator(file):
    #                     # print(read["header"].split(" ")[0][1:])
    #                     raw_name = seq_sum_data[read["header"].split()[0][1:]]
    #                     assert input_reads[raw_name] == 0
    #                     input_reads[raw_name] = 1
    # print(input_reads)
    # for key, value in input_reads.items():
    #     # try:
    #     assert value == 1
        # except AssertionError:
        #     print("error")
        #     print(key, value)


def test_collapse_data():
    save_path = Path('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_test')
    if save_path.exists() is False:
        raise IOError("There is no data to collapse")
    tmp_dir = save_path.parent.joinpath("tmp")#Path("/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy")#save_path.parent.joinpath("tmp")
    if tmp_dir.exists() is False:
        tmp_dir.mkdir()
    for i in os.listdir(str(save_path)):
        shutil.copytree(str(save_path.joinpath(i)), str(tmp_dir.joinpath(i)))
    collapse_data(save_path)
    collapsed_reads = {}
    for dir_name, subdirs, files in os.walk(str(save_path.joinpath("workspace"))):
        if Path(dir_name).parent.name == "workspace":
            collapsed_reads[Path(dir_name).name] = {}
        for file in files:
            if ".fastq" in Path(file).suffixes:
                fq = str(Path(dir_name).joinpath(file))
                with open(fq, 'r') as file:
                    for read in fastq_read_generator(file):
                        read_name = read["header"].split()[0][1:]
                        read_len = len(read["sequence"])
                        collapsed_reads[Path(dir_name).name][(read_name, read_len)] = 0
    #print(collapsed_reads)
    for dir_name, subdirs, files in os.walk(str(tmp_dir)):
        for file in files:
            if ".fastq" in Path(file).suffixes:
                fq = str(Path(dir_name).joinpath(file))
                with open(fq, 'r') as file:
                    for read in fastq_read_generator(file):
                        read_name = read["header"].split()[0][1:]
                        read_len = len(read["sequence"])
                        assert collapsed_reads[Path(dir_name).name][(read_name, read_len)] == 0
                        collapsed_reads[Path(dir_name).name][(read_name, read_len)] = 1


    for key in collapsed_reads:
        for key, value in collapsed_reads[key].items():
            assert value == 1


########################################################################
### Test Albacore Remote                                             ###
########################################################################

def test_albacore_binary():
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    flowcell = 'FLO-MIN106'
    input_path = "test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass/"
    expected_stdout = b'usage: read_fast5_basecaller.py [-h] [-l] [-v] [-i INPUT] -t WORKER_THREADS -s\n                                SAVE_PATH [--resume [X]] [-f FLOWCELL]\n                                [-k KIT] [--barcoding] [-c CONFIG]\n                                [-d DATA_PATH] [-b] [-r]\n                                [-n FILES_PER_BATCH_FOLDER] [-o OUTPUT_FORMAT]\n                                [-q READS_PER_FASTQ_BATCH]\n                                [--disable_filtering] [--disable_pings]\n\nONT Albacore Sequencing Pipeline Software\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -l, --list_workflows  List standard flowcell / kit combinations.\n  -v, --version         Print the software version.\n  -i INPUT, --input INPUT\n                        Folder containing read single_read_fast5 files (if not present,\n                        will expect file names on stdin).\n  -t WORKER_THREADS, --worker_threads WORKER_THREADS\n                        Number of worker threads to use.\n  -s SAVE_PATH, --save_path SAVE_PATH\n                        Path to save output.\n  --resume [X]          Resume previous run for the given save path. Optional\n                        parameter X is for debugging purposes only.\n  -f FLOWCELL, --flowcell FLOWCELL\n                        Flowcell used during the sequencing run.\n  -k KIT, --kit KIT     Kit used during the sequencing run.\n  --barcoding           Search for barcodes to demultiplex sequencing data.\n  -c CONFIG, --config CONFIG\n                        Optional configuration file to use.\n  -d DATA_PATH, --data_path DATA_PATH\n                        Optional path to model files.\n  -b, --debug           Output additional debug information to the log.\n  -r, --recursive       Recurse through subfolders for input data files.\n  -n FILES_PER_BATCH_FOLDER, --files_per_batch_folder FILES_PER_BATCH_FOLDER\n                        Maximum number of files in each batch subfolder. Set\n                        to 0 to disable batch subfolders.\n  -o OUTPUT_FORMAT, --output_format OUTPUT_FORMAT\n                        desired output format, can be fastq,single_read_fast5 or only one\n                        of these.\n  -q READS_PER_FASTQ_BATCH, --reads_per_fastq_batch READS_PER_FASTQ_BATCH\n                        number of reads per FastQ batch file. Set to 1 to\n                        receive one reads per file and file names which\n                        include the read ID. Set to 0 to have all reads per\n                        run ID written to one file.\n  --disable_filtering   Disable filtering into pass/fail folders\n  --disable_pings       Do not send summary information about the run\n'

    albacore = AlbacoreBasecaller(client=None, expected_workers=None, input_path=input_path,
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format="",
                                  reads_per_fastq=1000)
    func = albacore.command_function(stdout=subprocess.PIPE)
    comp_process = func(["read_fast5_basecaller.py", "--help"])
    assert comp_process.stdout == expected_stdout


def test_albacore_remote_basecall():
    save_path = Path('test_data/basecalled_data/results/local_basecall_test')
    if save_path.exists():
        shutil.rmtree(str(save_path))
    save_path.mkdir()

    flowcell = 'FLO-MIN106'
    input_path = Path('test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass')
    kit = 'SQK-LSK109'
    output_format = 'fastq'

    config = Configuration(config="test_configs/remote_builds.yml")
    compute_config = config.get_compute("cluster1")
    cluster = Cluster(compute_config, umass_mem=2480, logs=True)
    scheduler_address = cluster.connect()
    client = Client(scheduler_address)

    expected_workers = cluster.expected_workers

    albacore = AlbacoreBasecaller(client=client, expected_workers=expected_workers, input_path=input_path,
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format=output_format,
                                  reads_per_fastq=1000)
    albacore()

    input_reads = {}
    for batch in os.listdir(str(save_path)):
        if batch[0] == ".":
            continue
        for read in os.listdir(str(input_path.joinpath(batch))):
            input_reads[read] = 0

        path = save_path.joinpath(batch)
        seq_sum = str(path.joinpath("sequencing_summary.txt"))
        with open(seq_sum, 'r') as f:
            seq_sum_data = {}
            csv_reader = csv.reader(f, delimiter="\t")
            for i, row in enumerate(csv_reader):
                # print(row)
                seq_sum_data[row[1]] = row[0]

        f.close()

        for dir_name, subdirs, files in os.walk(str(path.joinpath("workspace"))):
            # print(dir_name)
            for file in files:
                # print(file)
                if ".fastq" in Path(file).suffixes:
                    fq = str(Path(dir_name).joinpath(file))
                    with open(fq, 'r') as file:
                        for read in fastq_read_generator(file):
                            # print(read["header"].split(" ")[0][1:])
                            raw_name = seq_sum_data[read["header"].split()[0][1:]]
                            assert input_reads[raw_name] == 0
                            input_reads[raw_name] = 1

    for key, value in input_reads.items():
        # try:
        assert value == 1
        # except AssertionError:
        #     print("error")
        #     print(key, value)


def test_collapse_remote_data():
    save_path = Path('test_data/basecalled_data/results/local_basecall_test')
    if save_path.exists() is False:
        raise IOError("There is no data to collapse")
    tmp_dir = save_path.parent.joinpath("tmp")#Path("/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy")#save_path.parent.joinpath("tmp")
    if tmp_dir.exists() is False:
        tmp_dir.mkdir()
    for i in os.listdir(str(save_path)):
        shutil.copytree(str(save_path.joinpath(i)), str(tmp_dir.joinpath(i)))
    collapse_data(save_path)
    collapsed_reads = {}
    for dir_name, subdirs, files in os.walk(str(save_path.joinpath("workspace"))):
        if Path(dir_name).parent.name == "workspace":
            collapsed_reads[Path(dir_name).name] = {}
        for file in files:
            if ".fastq" in Path(file).suffixes:
                fq = str(Path(dir_name).joinpath(file))
                with open(fq, 'r') as file:
                    for read in fastq_read_generator(file):
                        read_name = read["header"].split()[0][1:]
                        read_len = len(read["sequence"])
                        collapsed_reads[Path(dir_name).name][(read_name, read_len)] = 0
    #print(collapsed_reads)
    for dir_name, subdirs, files in os.walk(str(tmp_dir)):
        for file in files:
            if ".fastq" in Path(file).suffixes:
                fq = str(Path(dir_name).joinpath(file))
                with open(fq, 'r') as file:
                    for read in fastq_read_generator(file):
                        read_name = read["header"].split()[0][1:]
                        read_len = len(read["sequence"])
                        assert collapsed_reads[Path(dir_name).name][(read_name, read_len)] == 0
                        collapsed_reads[Path(dir_name).name][(read_name, read_len)] = 1


    for key in collapsed_reads:
        for key, value in collapsed_reads[key].items():
            assert value == 1



########################################################################
### Test Guppy                                                       ###
########################################################################
def test_guppy_basecaller():
    flowcell = 'FLO-MIN106'
    batches = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    fast5_out = False
    input_path = ''

    config = Configuration(config="test_configs/remote_builds.yml")
    compute_config = config.get_compute("cluster2")
    cluster = Cluster(compute_config, umass_mem=2480, logs=True)
    scheduler_address = cluster.connect()
    client = Client(scheduler_address)

    expected_workers = cluster.expected_workers

    guppy = GuppyBasecaller(client=client, expected_workers=expected_workers, input_path=input_path,
                 flowcell=None, kit=None, save_path=None, fast5_out=None,
                 reads_per_fastq=1000, worker_client=None, pull_link=None,
                 image_path=None, bind=None, cpu_threads_per_caller=1)



def fastq_read_generator(fastq):
    fastq_row = file_row_generator(fastq)
    fastq_data = {"header": "",
                  "sequence": "",
                  "quality": ""}
    seq_added = False
    while True:
        try:
            row = next(fastq_row)
            if row[0] == '@':
                if seq_added:
                    yield fastq_data
                    seq_added = False
                fastq_data = {"header": row,
                              "sequence": "",
                              "quality": ""}
            elif row[0] == "":
                continue
            elif row[0] == "+":
                fastq_data["quality"] = next(fastq_row)
            else:
                fastq_data["sequence"] = row
                seq_added = True
        except StopIteration:
            yield fastq_data
            break


def file_row_generator(file):
    for row in file:
        yield row






if __name__ == '__main__':
    test_albcore_build_command()
    test_albacore_batches()
    #test_albacore_binary()
    test_albacore_basecall()
    #test_collapse_data()

