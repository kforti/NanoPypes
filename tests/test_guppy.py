from pathlib import Path

from nanopypes.pipes.basecaller import GuppyBasecaller
from compute import Cluster
from config import Configuration

from distributed import Client

def test_guppy_batches():
    flowcell = 'FLO-MIN106'
    input_path = 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    fast5_out = False

    guppy = GuppyBasecaller(client=None, expected_workers=10, input_path=input_path,
                 flowcell=flowcell, kit=kit, save_path=save_path, fast5_out=fast5_out,
                worker_client='singularity', pull_link='docker://genomicpariscentre/guppy',
                bind='/project/umw_athma_pai/kevin')
    for batch in guppy.batches:
        cmd = guppy.build_command_pattern(kit, flowcell, batch, reads_per_fastq=100, fast5_out=False,
                                    adapter_trimming=False)
        cmd = cmd.format(save_path=Path(save_path).joinpath(batch.name), input_path=Path(input_path).joinpath(batch.name))
        print(cmd)

def test_guppy_basecall():
    flowcell = 'FLO-MIN106'
    input_path = 'test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'
    save_path = 'test_data/basecalled_data/results/local_basecall_test'
    kit = 'SQK-LSK109'
    fast5_out = False

    config = Configuration(config="test_configs/remote_builds.yml")
    compute_config = config.get_compute("cluster1")
    cluster = Cluster(compute_config, umass_mem=10000, logs=True)
    scheduler_address = cluster.connect()
    client = Client(scheduler_address)

    num_workers = cluster.expected_workers

    guppy = GuppyBasecaller(client=client, expected_workers=num_workers, input_path=input_path,
                            flowcell=flowcell, kit=kit, save_path=save_path, fast5_out=fast5_out,
                            worker_client='singularity', image_path='genomicpariscentre-guppy.sif',
                            bind='/project/umw_athma_pai/kevin')
    guppy()

if __name__ == '__main__':
    #test_guppy_batches()
    test_guppy_basecall()


