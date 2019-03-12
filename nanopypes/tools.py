from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes import AlbacoreBasecall


def basecall(config, data_splits, basecaller='Albacore'):
    if basecaller == 'Albacore':
        albacore = Albacore(config)
        compute = Cluster(config)
        compute.connect()
        basecaller = AlbacoreBasecall(albacore=albacore, compute=compute, data_splits=data_splits)
        basecalled_data = basecaller.execute()
        basecaller.remove_parallel_data()

    return basecalled_data
