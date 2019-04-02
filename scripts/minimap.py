from nanopypes.pipes.minimap2 import MiniMap2
from nanopypes.compute import Cluster
from nanopypes.config import Configuration


if __name__ == '__main__':

    config = Configuration("/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_configs/local_basecall.yml")
    compute_configs = config.compute
    compute = Cluster(compute_configs[0])
    client = compute.connect()

    minimapper = MiniMap2(input_path='/Users/kevinfortier/Desktop/t_variant_calling/data/external/malaria_SciRep2018/R7.3_fastq',
                          reference='/Users/kevinfortier/Desktop/t_variant_calling/data/external/malaria_SciRep2018/ref_genomes/Plasmodium_falciparum_3D7.fasta',
                          save_path='/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/minimap',
                          client=client,
                          command='splice')
    minimapper()
