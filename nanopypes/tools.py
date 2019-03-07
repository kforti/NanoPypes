from nanopypes.compute import Cluster
from nanopypes.oxnano import Albacore
from nanopypes.pipes import AlbacoreBasecall


def basecall(config, basecaller='Albacore'):
    if basecaller == 'Albacore':
        albacore = Albacore(config)
        cluster = Cluster(config)
        basecaller = AlbacoreBasecall(albacore=albacore, compute=cluster)
        data = basecaller.execute()

    return data
