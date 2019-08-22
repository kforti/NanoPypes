from nanopypes.utilities import PipelineConfiguration
from nanopypes.core.compute import ClusterManager
from nanopypes.core.pipeline_builder import PipelineBuilder


def build_pipeline(inputs, config):

    num_batches = len(inputs)
    #config = Configuration(config)
    pb = PipelineBuilder(inputs,
                         pipe_specs=config.pipe_configs,
                         pipeline_name="demultiplex",
                         pipeline_order=config.pipeline_order,
                         num_batches=num_batches)
    pb.build_tasks()
    pb.build_pipeline()
    pipeline = pb.pipeline
    #executor = DaskExecutor(cm.cluster.scheduler_address)

    return pb, config

def build_cluster(config):
    cm = ClusterManager.from_dict(config.compute_config)
    client = cm.start_cluster()
    return cm, client

def run_pipeline(pipeline, cm):
    state = pipeline.run()
    serialized_pipeline = pipeline.serialize()

    if state.is_fail():
        pass


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



import yaml



