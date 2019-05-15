from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes.basecaller import AlbacoreBasecaller, GuppyBasecaller, collapse_data
from nanopypes.pipes.parallel_rsync import ParallelRsync
from nanopypes.pipes.minimap2 import MiniMap2
from nanopypes.config import Configuration

from distributed import Client

from pathlib import Path

from dask.distributed import LocalCluster, Client


def albacore_basecaller(kit, flowcell, input_path, save_path, output_format, expected_workers, scheduler_address=None, client=None):
    """Function for running the parallel albacore basecaller"""
    ## Set configurations and build classes
    if client == None and scheduler_address:
        client = Client(scheduler_address)
    elif client == None and scheduler_address == None:
        raise ValueError("You must pass either a scheduler address or client to run this Pipe")
    albacore = Albacore(
                       kit=kit,
                       flowcell=flowcell,
                       input_path=input_path,
                       save_path=save_path,
                       output_format=output_format)

    basecall = AlbacoreBasecaller(albacore=albacore, client=client, expected_workers=expected_workers)
    basecall()
    save_path = Path(save_path)
    print("collapsing data")
    collapse_data(save_path)

    return


def guppy_basecaller(expected_workers, input_path=None, flowcell=None,
                     kit=None, save_path=None, fast5_out=None, reads_per_fastq=1000,
                     worker_client=None, pull_link=None, image_path=None,
                     bind=None, client=None, cpu_threads_per_caller=1):
    guppy = GuppyBasecaller(client=client, expected_workers=expected_workers, input_path=input_path,
                            flowcell=flowcell, kit=kit, save_path=save_path, fast5_out=fast5_out,
                            reads_per_fastq=reads_per_fastq, worker_client=worker_client, pull_link=pull_link,
                            image_path=image_path, bind=bind)
    guppy()


def parallel_rsync(local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):
    if client == 'local':
        client = Client(LocalCluster())

    pr = ParallelRsync(local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction, client=client)
    pr()

    return


def parallel_minimap2(input_path, reference, save_path, command, scheduler_address=None, client=None):
    if client == None and scheduler_address:
        client = Client(scheduler_address)
    elif client == None and scheduler_address == None:
        raise ValueError("You must pass either a scheduler address or client to run this Pipe")

    mmap = MiniMap2(input_path=input_path, reference=reference, command=command, client=client)
    mmap()

    return
