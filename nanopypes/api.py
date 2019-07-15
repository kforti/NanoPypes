import yaml

from nanopypes.utilities import Configuration
from nanopypes.compute import ClusterManager
from nanopypes.distributed_data.pipeline_data import PipelineData
from nanopypes.pipelines.pipeline_builder import PipelineBuilder

from prefect.engine.executors.dask import DaskExecutor


def build_config(path, user_input={}):
    config = Configuration(path, user_input)
    return config


def build_pipeline(config):
    #config = Configuration(config)
    cm = ClusterManager.from_dict(config.compute_config)
    pd = PipelineData(input_path="/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/",
                      cluster_manager=cm, pipe_specs=config.pipe_configs)
    pb = PipelineBuilder(pipeline_name="demultiplex",
                         pipeline_order=config.pipeline_order,
                         pipeline_data=pd)
    pb.build_pipeline()
    pipeline = pb.pipeline
    executor = None#DaskExecutor(cm.cluster.scheduler_address)

    return pb, executor


def run_pipeline(pipeline_builder):
    pipeline_builder.run()


if __name__ == '__main__':
    from distributed import LocalCluster
    from prefect.engine.executors.dask import DaskExecutor

    cluster = LocalCluster()
    executor = DaskExecutor(address=cluster.scheduler_address)
    user_input = {'flowcell': 'FLO-MIN106', 'kit': 'SQK-LSK109', 'reference': '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/sequence.txt'}
    config = build_config("/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_configs/local_pipeline.yml", user_input)
    pb, executor = build_pipeline(config)
    print(pb.pipeline.tasks)
    #pb.pipeline.run(executor=executor)
    pb.pipeline.visualize()
    #pb.pipeline.run(executor=executor)

    for edge in pb.pipeline.edges:
        print(edge)



    # def build_config(path):
    #     config = Configuration(path)
    #     return config
    #
    #
    # def build_pipeline(compute_config, input_path, save_path, pipe_configs):
    #
    #     cm = ClusterManager.from_dict(compute_config)
    #
    #     pb = PipelineBuilder(cluster_manager=cm,
    #                          input_path=input_path,
    #                          save_path=save_path,
    #                          pipe_configs=pipe_configs)
    #     pb.build_pipeline()
    #     pipeline = pb.pipeline
    #
    #     for cmd, commands in pb.all_commands.items():
    #         print(cmd, commands)
    #
    #     return pipeline, pb.all_commands

