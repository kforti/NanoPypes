from datetime import datetime
import shutil
import os
from pathlib import Path
import subprocess

from nanopypes.pipes.basecaller import AlbacoreBasecaller
from compute import Cluster
from nanopypes.pipes.basecaller import collapse_data

from distributed import Client

import logging



logging.basicConfig(filename='app.log', filemode='a', level="INFO", format='%(name)s - %(levelname)s - %(message)s')


def nanopypes_albacore_test_run(save_path, input_path, cores, mem, job_ncpus, job_memory, workers, umass_mem, scale_value):
    flowcell = 'FLO-MIN106'
    kit = 'SQK-LSK109'
    output_format = 'fastq'

    cluster = Cluster(queue='short', project='/project/umw_athma_pai', job_time='3:00', cores=cores, mem=mem,
                 ncpus=job_ncpus, memory=job_memory, workers=workers, scale_value=scale_value, cluster_type="LSF", umass_mem=umass_mem,
                 time_out=2000, logs=False)
    scheduler_address = cluster.connect()
    client = Client(scheduler_address)
    expected_workers = cluster.expected_workers

    # Run Local
    # cluster = LocalCluster()
    # client = Client(cluster)
    # expected_workers = 4

    albacore = AlbacoreBasecaller(client=client, expected_workers=expected_workers, input_path=input_path,
                                  flowcell=flowcell, kit=kit, save_path=save_path, output_format=output_format,
                                  reads_per_fastq=1000)
    albacore()
    collapse_data(save_path)


def albacore_test_run(job_script_path):
    cmd = "bsub < {script_path}".format(script_path=job_script_path)
    process = subprocess.run(cmd, shell=True)
    return


def batches_to_dir(input_batches, dir_path):
    if dir_path.exists() is False:
        dir_path.mkdir()
    batches_in_dir_path = os.listdir(str(dir_path))
    for batch in input_batches:
        if batch.name in batches_in_dir_path:
            continue
        else:
            shutil.move(str(batch), str(dir_path))


def dir_to_batches(dir_path):
    for batch in os.listdir(str(dir_path)):
        shutil.move(str(dir_path.joinpath(batch), str(dir_path.parent.joinpath(batch))))


def run_test(test_name, mem, cores, job_ncpus, job_memory, workers, umass_mem, job_script_path, scale_value):
    nanopypes_save_path = Path(test_path).joinpath('nanopypes', test_name)
    cmdline_save_path = Path(test_path).joinpath('without_nanopypes', test_name)
    input_path = Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test')
    input_batches = os.listdir(str(input_path))
    logging.info(
        'Albacore Nanopypes - Status: {status}\tInput_batches {input_batches}\tSave_path {save_path}\tMem {mem}\tCores {cores}\tJob_ncpus {job_ncpus}\tJob_memory {job_memory}\tWorkers {workers}\tUmass_mem {umass_mem}\tTime {time}'.format(
            status='start', input_batches=input_batches, save_path=nanopypes_save_path, mem=mem, cores=cores,
            job_ncpus=job_ncpus, job_memory=job_memory, workers=workers, umass_mem=umass_mem, time=datetime.now()))

    nanopypes_albacore_test_run(save_path=nanopypes_save_path, input_path=input_path, cores=cores,
                                mem=mem, job_ncpus=job_ncpus, job_memory=job_memory, workers=workers,
                                umass_mem=umass_mem, scale_value=scale_value)

    logging.info(
        'Albacore Nanopypes - Status: {status}\tInput_batches {input_batches}\tSave_path {save_path}\tMem {mem}\tCores {cores}\tJob_ncpus {job_ncpus}\tJob_memory {job_memory}\tWorkers {workers}\tUmass_mem {umass_mem}\tTime {time}'.format(
            status='finished', input_batches=input_batches, save_path=nanopypes_save_path, mem=mem, cores=cores,
            job_ncpus=job_ncpus,
            job_memory=job_memory, workers=workers, umass_mem=umass_mem, time=datetime.now()))

    logging.info(
        'Albacore Commandline - Status: {status}\tInput_batches {input_batches}\tSave_path {save_path}\tMem {mem}\tCores {cores}\tJob_ncpus {job_ncpus}\tJob_memory {job_memory}\tThreads {threads}\tUmass_mem {umass_mem}\tTime {time}'.format(
            status='start', input_batches=input_batches, save_path=cmdline_save_path, mem=mem, cores=cores,
            job_ncpus=job_ncpus, job_memory=job_memory, threads=workers, umass_mem=umass_mem, time=datetime.now()))

    albacore_test_run(job_script_path)

    logging.info(
        'Albacore Commandline - Status: {status}\tInput_batches {input_batches}\tSave_path {save_path}\tMem {mem}\tCores {cores}\tJob_ncpus {job_ncpus}\tJob_memory {job_memory}\tThreads {threads}\tUmass_mem {umass_mem}\tTime {time}'.format(
            status='finished', input_batches=input_batches, save_path=cmdline_save_path, mem=mem, cores=cores,
            job_ncpus=job_ncpus,
            job_memory=job_memory, threads=workers, umass_mem=umass_mem, time=datetime.now()))

if __name__ == '__main__':

    test_path = '/project/umw_athma_pai/kevin/data/Albacore_tests/'
    job_scrips = ["test_job_scripts/albacore_test1.sh",
                  "test_job_scripts/albacore_test2.sh",
                  "test_job_scripts/albacore_test3.sh",
                  "test_job_scripts/albacore_test4.sh",
                  "test_job_scripts/albacore_test5.sh",
                  "test_job_scripts/albacore_test6.sh"]
    times = {}
    test_names = ["test1", "test2", "test3", "test4", "test5", "test6"]
    workers_list = [5, 10, 20, 30, 20, 25]
    umass_mem_list = [10240, 20480, 40960, 61440, 40960, 51200]
    mem_list = [10589934592, 10589934592 * 2, 10589934592 * 4, 10589934592 * 6, 10589934592 * 4, 10589934592 * 5]
    job_ncpus_list = [5, 10, 20, 30, 20, 25]
    job_memory_list = ['10 GB', '20 GB', '40 GB', '60 GB', '40 GB', '50 GB']
    cores_list = [5, 10, 20, 30, 20, 25]
    scale_values = [5, 10, 20, 30, 40, 50]

    ###############################
    ### Test1                   ###
    ###############################
    #Move batches to seperate dir
    TEST_NUM = 0
    input_paths = PATHS["nanopypes"]["test1"]
    batches_to_dir(input_paths, dir_path=Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test'))
    run_test(test_name=test_names[TEST_NUM],
             mem=mem_list[TEST_NUM],
             cores=cores_list[TEST_NUM],
             job_ncpus=job_ncpus_list[TEST_NUM],
             job_memory=job_memory_list[TEST_NUM],
             workers=workers_list[TEST_NUM],
             umass_mem=umass_mem_list[TEST_NUM],
             job_script_path=job_scrips[TEST_NUM],
             scale_value=scale_values[TEST_NUM]
             )

    # # save_paths = paths["test1"]["dests"]
    #
    # # Test1 Without NanoPypes
    #
    # "BSUB -q 3:00 -p /project/umw_athma_pai -n"

    ###############################
    ### Test2                   ###
    ###############################
    TEST_NUM = 1
    input_paths = PATHS["nanopypes"]["test2"]
    batches_to_dir(input_paths,
                   dir_path=Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test'))
    run_test(test_name=test_names[TEST_NUM],
             mem=mem_list[TEST_NUM],
             cores=cores_list[TEST_NUM],
             job_ncpus=job_ncpus_list[TEST_NUM],
             job_memory=job_memory_list[TEST_NUM],
             workers=workers_list[TEST_NUM],
             umass_mem=umass_mem_list[TEST_NUM],
             job_script_path=job_scrips[TEST_NUM],
             scale_value=scale_values[TEST_NUM]
             )

    ###############################
    ### Test3                   ###
    ###############################
    TEST_NUM = 2
    input_paths = PATHS["nanopypes"]["test3"]
    batches_to_dir(input_paths,
                   dir_path=Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test'))
    run_test(test_name=test_names[TEST_NUM],
             mem=mem_list[TEST_NUM],
             cores=cores_list[TEST_NUM],
             job_ncpus=job_ncpus_list[TEST_NUM],
             job_memory=job_memory_list[TEST_NUM],
             workers=workers_list[TEST_NUM],
             umass_mem=umass_mem_list[TEST_NUM],
             job_script_path=job_scrips[TEST_NUM],
             scale_value=scale_values[TEST_NUM]
             )

    ###############################
    ### Test4                   ###
    ###############################
    TEST_NUM = 3
    input_paths = PATHS["nanopypes"]["test4"]
    batches_to_dir(input_paths,
                   dir_path=Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test'))
    run_test(test_name=test_names[TEST_NUM],
             mem=mem_list[TEST_NUM],
             cores=cores_list[TEST_NUM],
             job_ncpus=job_ncpus_list[TEST_NUM],
             job_memory=job_memory_list[TEST_NUM],
             workers=workers_list[TEST_NUM],
             umass_mem=umass_mem_list[TEST_NUM],
             job_script_path=job_scrips[TEST_NUM],
             scale_value=scale_values[TEST_NUM]
             )

    ###############################
    ### Test5                   ###
    ###############################
    TEST_NUM = 4
    input_paths = PATHS["nanopypes"]["test5"]
    batches_to_dir(input_paths,
                   dir_path=Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test'))
    run_test(test_name=test_names[TEST_NUM],
             mem=mem_list[TEST_NUM],
             cores=cores_list[TEST_NUM],
             job_ncpus=job_ncpus_list[TEST_NUM],
             job_memory=job_memory_list[TEST_NUM],
             workers=workers_list[TEST_NUM],
             umass_mem=umass_mem_list[TEST_NUM],
             job_script_path=job_scrips[TEST_NUM],
             scale_value=scale_values[TEST_NUM]
             )

    ###############################
    ### Test6                   ###
    ###############################
    TEST_NUM = 5
    input_paths = PATHS["nanopypes"]["test6"]
    batches_to_dir(input_paths,
                   dir_path=Path('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test'))
    run_test(test_name=test_names[TEST_NUM],
             mem=mem_list[TEST_NUM],
             cores=cores_list[TEST_NUM],
             job_ncpus=job_ncpus_list[TEST_NUM],
             job_memory=job_memory_list[TEST_NUM],
             workers=workers_list[TEST_NUM],
             umass_mem=umass_mem_list[TEST_NUM],
             job_script_path=job_scrips[TEST_NUM],
             scale_value=scale_values[TEST_NUM]
             )