from nanopypes.pipelines.pipeline_builder import PipelineBuilder
from nanopypes.utilities import PipelineConfiguration
from nanopypes.compute import ClusterManager
import time
import argparse
import os

from prefect.engine.executors.dask import DaskExecutor



def test_pipeline_builder_remote(config_path, input_path):
    user_input = {'flowcell': 'FLO-MIN106',
                  'kit': 'SQK-LSK109',
                  'reference': '/project/umw_athma_pai/genomes/ercc/ERCC92.fa'}
    config = PipelineConfiguration(config_path, user_input)
    cluster_manager = ClusterManager.from_dict(config.compute_config)
    cluster_manager.build_cluster()
    cluster_manager.start_cluster()
    executor = DaskExecutor(cluster_manager.cluster.scheduler_address)

    inputs = [input_path]
    pipe_specs = config.pipe_configs
    print(pipe_specs)
    time.sleep(30)
    pb = PipelineBuilder(inputs=inputs,
                         pipeline_order=config.pipeline_order,
                         pipeline_name="test-pipeline",
                         partitions=250,
                         pipe_specs=pipe_specs)
    pb.build_tasks()
    pb.build_pipeline()
    print(vars(pb.pipeline))
    pb.pipeline.run(executor=executor)


def set_envs():
    minimap_save_path = "/nl/umw_athma_pai/kevin/test_ercc/map"
    basecall_save_path = "/nl/umw_athma_pai/kevin/test_ercc/basecall"
    print([str(i) for i in os.scandir(minimap_save_path)])
    print([str(i) for i in os.scandir(basecall_save_path)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Push code to cluster.')
    parser.add_argument("--config_path")
    parser.add_argument("--input_path")
    args = parser.parse_args()
    config_path = args.config_path
    input_path = args.input_path
    set_envs()
    test_pipeline_builder_remote(config_path, input_path)

