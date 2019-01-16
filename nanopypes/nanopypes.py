import argparse
import os
from pathlib import Path
from albacore import Albacore, Basecaller
from data_types import RawData
from basecall_config import BASECALLER_CONFIG as config

def basecall(input, flowcell, kit, save_path, output_format, queue, project, job_time, initial_workers, cores, memory,
             cluster_type="LSF",
             barcoding=None,
             reads_per_fastq=1000):
    """ function for running the albacore basecaller in parallel on a cluster.
    """

    albacore = Albacore(input=input,
                        flowcell=flowcell,
                        kit=kit,
                        save_path=save_path,
                        output_format=output_format,
                        barcoding=barcoding,
                        reads_per_fastq=reads_per_fastq)

    cb = ClusterBasecaller(albacore=albacore,
                           queue=queue,
                           project=project,
                           job_time=job_time,
                           initial_workers=initial_workers,
                           cores=cores,
                           memory=memory)
    cb.parallel_basecaller()


if __name__ == '__main__':
    # path = Path('./test_data')
    # for i in range(10):
    #     d = str(i)
    #     dir = path.joinpath(d)
    #     dir.mkdir()
    #     for y in range(500):
    #         n = str(y)
    #         n_p = dir.joinpath(n)
    #         with open(n_p, 'w') as f:
    #             f.write('some data')

    ###########################################################################################################
    # Raw Fast5 Data
    ###########################################################################################################
    input_path = config["input_path"]
    fast5 = RawData(input_path)

    ###########################################################################################################
    # Albacore
    ###########################################################################################################
    kit = config["kit"]
    save_path = config["save_path"]
    flowcell = config["flowcell"]
    barcoding = config["barcoding"]
    worker_threads = config["worker_threads"]
    output_format = config["output_format"]
    recursive = config["recursive"]

    ###########################################################################################################
    # ClusterBasecaller
    ###########################################################################################################

    queue = config["queue"]
    project = config["project"]
    job_time = config["job_time"]
    workers = config["workers"]
    ncpus = config["ncpus"]
    mem = config["mem"]
    cores = config["cores"]
    memory = config["memory"]



    basecall(input=fast5,
             flowcell=flowcell,
             kit=kit,
             save_path=save_path,
             output_format=output_format,
             queue=queue,
             project=project,
             job_time=job_time,
             initial_workers=workers,
             cores=cores,
             memory=memory,
             cluster_type="LSF",
             barcoding=None,
             reads_per_fastq=1000)
