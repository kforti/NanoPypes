from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes.basecaller2 import AlbacoreBasecaller
from nanopypes.pipes.parallel_rsync import ParallelRsync
from nanopypes.config import Configuration

from asyncio.futures import CancelledError

from dask.distributed import LocalCluster, Client


def albacore_basecaller(config, kit, flowcell, input_path, save_path, output_format):
    """Function for running the parallel albacore basecaller"""
    ## Set configurations and build classes
    config = Configuration(config)
    compute_configs = config.compute
    compute = Cluster(compute_configs[0])
    albacore = Albacore(config=config,
                       kit=kit,
                       flowcell=flowcell,
                       input_path=input_path,
                       save_path=save_path,
                       output_format=output_format)

    basecall = AlbacoreBasecaller(albacore=albacore, compute=compute)
    basecall()

    compute.close()

    return


def parallel_rsync(local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):
    if client == 'local':
        client = Client(LocalCluster())

    pr = ParallelRsync(local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction, client=client)
    pr()

    return


