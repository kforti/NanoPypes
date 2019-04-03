from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes.basecaller import AlbacoreBasecaller
from nanopypes.config import Configuration

def albacore_basecaller(config, data_splits, batch_bunch, basecaller='albacore', continue_on=False, last_batch=None):
    config = Configuration(config)
    compute_configs = config.compute
    compute = Cluster(compute_configs[0])
    client = compute.connect()
    albacore = Albacore(config, continue_on=continue_on)
    basecall = AlbacoreBasecaller(albacore=albacore, client=client, num_splits=data_splits, batch_bunch_size=batch_bunch, continue_on=continue_on)
    basecall()
    compute.close()

    return
