from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes.basecaller2 import AlbacoreBasecaller
from nanopypes.pipes.parallel_rsync import ParallelRsync
from nanopypes.config import Configuration

from asyncio.futures import CancelledError

from dask.distributed import LocalCluster, Client


def albacore_basecaller(config, data_splits, batch_bunch, continue_on=False):
    """Function for running the parallel albacore basecaller"""
    ## Set configurations and build classes
    config = Configuration(config)
    compute_configs = config.compute
    compute = Cluster(compute_configs[0])
    client = compute.connect()
    albacore = Albacore(config, continue_on=continue_on)

    attempts = 0
    while attempts < 10:
        try:
            basecall = AlbacoreBasecaller(albacore=albacore, client=client, num_splits=data_splits, batch_bunch_size=batch_bunch, continue_on=continue_on)
            basecall()
        except CancelledError:
            print("There was an error in the basecaller. Restarting Now......")
            continue_on = True
            attempts += 1

    compute.close()

    return


def parallel_rsync(local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):
    if client == 'local':
        client = Client(LocalCluster())

    pr = ParallelRsync(local_path=local_path, remote_path=remote_path, password=password, rsync_options=rsync_options, direction=direction, client=client)
    pr()

    return


