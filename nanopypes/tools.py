from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes import AlbacoreBasecall
from nanopypes.config import Configuration

def basecall(config, data_splits, basecaller='albacore', continue_on=False, last_batch=None):
    config = Configuration(config)
    compute_configs = config.compute
    if basecaller == 'albacore':
        albacore = Albacore(config, continue_on=continue_on, last_batch=last_batch)
        compute = Cluster(compute_configs[0])
        compute.connect()
        basecaller = AlbacoreBasecall(albacore=albacore, compute=compute, data_splits=data_splits)
        basecalled_data = basecaller.execute()
        basecaller.remove_parallel_data()

    return basecalled_data
