from nanopypes.distributed_data.partition_data import merge_mapped_reads, merge_demultiplexed_data, partition_demultiplexed_data, partition_basecalled_data, partition_ont_seq_data, merge_basecalled_data

import os
from pathlib import Path



def _create_demultiplexed_data():
    path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data"
    barcodes = 6
    from pathlib import Path
    for i in range(10):
        batch_path = os.path.join(path, "batch_{}".format(str(i)))
        try:
            os.mkdir(batch_path)
        except FileExistsError:
            pass

        for i in range(barcodes):
            bc_name = "BC{}.fastq".format(str(i))
            bc_path = os.path.join(batch_path, bc_name)
            with open(bc_path, 'w') as file:
                file.write("Some data...")


#############################################################
### Test Functions                                        ###
#############################################################

def test_partition_seq_data():
    path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"
    partitions = 5
    results = partition_ont_seq_data(path, partitions, "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy")
    print(results[0])
    print(results[1])
    print(results[2])


def test_merge_basecalled_data():
    path = Path("/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy_2")
    merge_basecalled_data(path)


def test_partition_basecalled_data():
    inputs = [['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/9', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/0'],
              ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/7', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/6'],
              ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/8'],
              ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/4', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/3'],
              ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/2', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/5']]
    command_data = []
    input_batches = []
    save_batches = []
    for i, batch in enumerate(inputs):
        results = partition_basecalled_data(batch, batch_num=i, save_path=".")
        command_data.append(results[0])
        input_batches.append(results[1])
        save_batches.append(results[2])
    print(command_data)
    print(input_batches)
    print(save_batches)

def test_partition_basecalled_data_demultiplex():
    inputs = [[
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/9',
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/0'],
              [
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/7',
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/6'],
              [
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/1',
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/8'],
              [
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/4',
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/3'],
              [
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/2',
                  '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy/5']]
    command_data = []
    input_batches = []
    save_batches = []
    for i, batch in enumerate(inputs):
        results = partition_basecalled_data(batch, batch_num=i, save_path=".", input_type='main_dir')
        command_data.append(results[0])
        input_batches.append(results[1])
        save_batches.append(results[2])
    print(command_data)
    print(input_batches)
    print(save_batches)


def test_partition_demultiplexed_data():
    inputs = [['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_6'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_8', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_9'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_7', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_0'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_5', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_2'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_3', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_4']]

    command_data = []
    input_batches = []
    save_batches = []
    for i, batch in enumerate(inputs):
        results = partition_demultiplexed_data(batch, save_path=".")
        command_data.append(results[0])
        input_batches.append(results[1])
        save_batches.append(results[2])
    print(command_data)
    print(input_batches)
    print(save_batches)


def test_demultiplex_merge():
    inputs = [['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_1', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_6'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_8', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_9'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_7', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_0'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_5', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_2'], ['/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_3', '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data/batch_4']]

    merge_demultiplexed_data(inputs, "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplex_merge")


def test_mapped_reads_merge():
    inputs = [['./nanopypes_batch_0/ont_batch_9.sam', './nanopypes_batch_0/ont_batch_0.sam'], ['./nanopypes_batch_1/ont_batch_7.sam', './nanopypes_batch_1/ont_batch_6.sam'], ['./nanopypes_batch_2/ont_batch_1.sam', './nanopypes_batch_2/ont_batch_8.sam'], ['./nanopypes_batch_3/ont_batch_4.sam', './nanopypes_batch_3/ont_batch_3.sam'], ['./nanopypes_batch_4/ont_batch_2.sam', './nanopypes_batch_4/ont_batch_5.sam']]
    #merge_mapped_reads(inputs, )


def test_basecall_mapping_data_partition():
    path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"
    partitions = 5
    results = partition_ont_seq_data(path, partitions,
                                     "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy")

    inputs = results[2]
    command_data = []
    input_batches = []
    save_batches = []
    for i, batch in enumerate(inputs):
        results = partition_basecalled_data(batch, batch_num=i, save_path=".")
        command_data.append(results[0])
        input_batches.append(results[1])
        save_batches.append(results[2])
    print(command_data)
    print(input_batches)
    print(save_batches)

def test_basecall_demultiplex_mapping_data_partition():
    path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"
    partitions = 5
    results = partition_ont_seq_data(path, partitions,
                                     "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy")

    inputs = results[2]

    command_data = []
    input_batches = []
    save_batches = []
    for i, batch in enumerate(inputs):
        results = partition_basecalled_data(batch, input_type='main_dir', batch_num=i, save_path="/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data")
        command_data.append(results[0])
        input_batches.append(results[1])
        save_batches.append(results[2])
    print(command_data)
    print(input_batches)
    print(save_batches)

    inputs = save_batches
    command_data = []
    input_batches = []
    save_batches = []
    for i, batch in enumerate(inputs):
        results = partition_demultiplexed_data(batch, batch_num=i,
                                               save_path="/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/mapped_reads")
        command_data.append(results[0])
        input_batches.append(results[1])
        save_batches.append(results[2])
    print(command_data)
    print(input_batches)
    print(save_batches)


def test_data_partitioner():
    from nanopypes.distributed_data.partition_data import DataPartitioner

    from prefect import Flow


    results = []
    inputs = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"]
    pipeline = Flow('test-pipeline')
    save_path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy"
    partition_strategy = {'split/merge': 'one_to_many', 'method': '', 'partitions': 5}

    dp = DataPartitioner(inputs=inputs,
                         num_batches=1,
                         save_path=save_path,
                         data_type='ont_sequence',
                         pipeline=pipeline,
                         dependencies=None,
                         partition_strategy=partition_strategy,
                         name='test-task',
                         demultiplex=False)
    tasks1 = dp.partition_data()
    # with pipeline as flow:
    #     for t in tasks:
    #         print(t)
    #         result = t()
    #         results.append(result)


    partition_strategy = {'split/merge': 'one_to_one', 'method': '', 'partitions': 5}
    # inputs = []
    # with pipeline as flow:
    #     for i in range(5):
    #         inputs.append(tasks1[0]['saves'][i])
    dp = DataPartitioner(num_batches=5,
        #inputs=inputs,
                         save_path=save_path,
                         data_type='ont_basecalled',
                         pipeline=pipeline,
                         dependencies=results,
                         partition_strategy=partition_strategy,
                         name='test-task',
                         demultiplex=False)
    tasks = dp.partition_data()

    print(tasks)

    with pipeline as flow:
        result = tasks1[0](batch=inputs[0])
        saves = result['saves']
        inputs = []
        for i in range(5):
            tasks[i](batch=saves[i])

    pipeline.visualize()
    # print(vars(pipeline))
    pipeline.run()

def test_pipeline_builder():
    from nanopypes.distributed_data.pipeline_data import PipelineBuilder
    from nanopypes.utilities import Configuration


    path = "../nanopypes/configs/pipelines/pipeline.yml"
    user_input = {'flowcell': 'FLO-MIN106',
                  'kit': 'SQK-LSK109',
                  'reference': '/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/lambda_reference.fasta'}
    config = Configuration(path, user_input)

    inputs = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass"]
    pipe_specs = config.pipe_configs
    print(pipe_specs)
    pb = PipelineBuilder(inputs=inputs,
                         pipeline_order=config.pipeline_order,
                         pipeline_name="test-pipeline",
                         num_batches=1,
                         pipe_specs=pipe_specs)
    pb.build_tasks()
    print('provenance', pb.data_provenance)
    pb.build_pipeline()
    pb.pipeline.visualize()
    pb.pipeline.run()


def test_pipeline_builder_remote():
    from nanopypes.distributed_data.pipeline_data import PipelineBuilder
    from nanopypes.utilities import Configuration
    from nanopypes.compute import ClusterManager
    import time

    from prefect.engine.executors.dask import DaskExecutor


    path = "../nanopypes/configs/pipelines/remote_pipeline.yml"
    user_input = {'flowcell': 'FLO-MIN106',
                  'kit': 'SQK-LSK109',
                  'reference': '/project/umw_athma_pai/genomes/ercc/ERCC92.fa'}
    config = Configuration(path, user_input)
    cluster_manager = ClusterManager.from_dict(config.compute_config)
    cluster_manager.build_cluster()
    cluster_manager.start_cluster()
    executor = DaskExecutor(cluster_manager.cluster.scheduler_address)

    inputs = ["/nl/umw_athma_pai/kevin/test_ercc/inputs"]
    pipe_specs = config.pipe_configs
    print(pipe_specs)
    time.sleep(60)
    pb = PipelineBuilder(inputs=inputs,
                         pipeline_order=config.pipeline_order,
                         pipeline_name="test-pipeline",
                         num_batches=1,
                         pipe_specs=pipe_specs)
    pb.build_tasks()
    print('provenance', pb.data_provenance)
    pb.build_pipeline()
    print(vars(pb.pipeline))
    pb.pipeline.run(executor=executor)


if __name__ == '__main__':
    #test_partition_seq_data()
    #test_merge_basecalled_data()
    #test_partition_basecalled_data()
    #test_partition_basecalled_data_demultiplex()
    #test_partition_demultiplexed_data()
    #test_demultiplex_merge()
    #test_basecall_mapping_data_partition()
    #test_basecall_demultiplex_mapping_data_partition()
    #test_data_partitioner()
    #test_pipeline_builder()
    test_pipeline_builder_remote()
    #from prefect import Flow, task
    #
    # @task
    # def get_data():
    #     return {'data1': 2, 'data3': 4, 'data2': 8}
    #
    # @task
    # def transform_data(data):
    #     return data + 3
    #
    # with Flow('pipeline') as flow:
    #     data = get_data()
    #     result = data['data2']
    #     trans = transform_data(result)
    #
    # flow.run()



    # import os
    #
    # path = "/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/demultiplexed_data"
    # dirs = os.listdir(path)
    # inputs = []
    # batch = []
    # for i in dirs:
    #     batch.append(os.path.join(path, i))
    #     if len(batch) == 2:
    #         inputs.append(batch)
    #         batch = []
    # print(inputs)
