from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes import AlbacoreBasecaller
from nanopypes.config import Configuration

def basecall(config, data_splits, batch_bunch, basecaller='albacore', continue_on=False, last_batch=None):
    config = Configuration(config)
    compute_configs = config.compute
    compute = Cluster(compute_configs[0])
    client = compute.connect()
    albacore = Albacore(config)
    data = AlbacoreBasecaller.start(albacore, client, data_splits=data_splits, batch_bunch_size=batch_bunch, continue_on=continue_on)

    compute.close()

    return
