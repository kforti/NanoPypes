import yaml

from nanopypes.utilities import Configuration
from nanopypes.compute import ClusterManager
from nanopypes.pipelines.variant_caller import PipelineBuilder

def build_config(path):
    config = Configuration(path, {})
    return config


def build_pipeline(config):
    #config = Configuration(config)
    cm = ClusterManager.from_dict(config.compute_config)

    pb = PipelineBuilder(cluster_manager=cm,
                         input_path=config.input_path,
                         save_path=config.save_path,
                         pipe_configs=config.pipe_configs,
                         pipeline_order=config.pipeline_order)
    pb.build_pipeline()
    pipeline = pb.pipeline

    return pipeline, pb.all_commands


if __name__ == '__main__':
    config = build_config("/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/nanopypes/configs/pipelines/pipeline.yml")
    p, c = build_pipeline(config)
    print(p.__dict__)



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

