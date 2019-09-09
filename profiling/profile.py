from nanopypes.utilities import PipelineConfiguration
from nanopypes.core.pipeline_builder import PipelineBuilder
from distributed import LocalCluster
from prefect.engine.executors.dask import DaskExecutor

def run_pipeline():
    #cluster = LocalCluster()
    #executor = DaskExecutor(cluster.scheduler_address)

    pipeline_path = "../nanopypes/configs/pipelines/albacore_ercc.yml"
    compute_path = "../nanopypes/configs/compute.yml"
    compute_id = 'umass_ghpcc_lsf_basecall'
    user_input = {'flowcell': 'FLO-MIN106',
                  'kit': 'SQK-LSK109'}
    config = PipelineConfiguration(pipeline_path=pipeline_path, compute_config_path=compute_path, compute_id=compute_id, user_input=user_input)

    inputs = "../tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/single_read_fast5/pass"
    save_path = "../tests/test_data/test_pipeline"
    pipe_specs = config.pipe_configs
    print(pipe_specs)
    print("pipeline_order:", config.pipeline_order)
    pb = PipelineBuilder(inputs=inputs,
                         save_path=save_path,
                         pipeline_order=config.pipeline_order,
                         pipeline_name="test-pipeline",
                         pipe_specs=pipe_specs,
                         partitions=10)
    pb.build_tasks()
    # print('provenance', pb.data_provenance)
    pb.build_pipeline()
    #pb.pipeline.visualize()
    pb.pipeline.run() # executor=executor)


if __name__ == '__main__':
    run_pipeline()
