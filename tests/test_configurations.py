from nanopypes.utilities import Configuration



def test_compute_config():
    user_input = {'flowcell': 'ghkgk', 'kit': 'lknkl', 'reference': 'jhkjhkjhj'}
    config = Configuration("test_configs/local_pipeline.yml", user_input)
    print(config.compute_config)

def test_pipe_config():
    user_input = {'flowcell': 'ghkgk', 'kit': 'lknkl', 'reference': 'jhkjhkjhj'}
    config = Configuration("test_configs/local_pipeline.yml", user_input)
    print(config.pipe_configs)

def test_pipeline_config():
    user_input = {'flowcell': 'ghkgk', 'kit': 'lknkl', 'reference': 'jhkjhkjhj'}
    config = Configuration("test_configs/local_pipeline.yml", user_input)
    print(config.pipeline_config)

def test_remote_compute_config():
    from nanopypes.compute import ClusterManager
    user_input = {'flowcell': 'ghkgk', 'kit': 'lknkl', 'reference': 'jhkjhkjhj'}
    config = Configuration("../nanopypes/configs/pipelines/remote_pipeline.yml", user_input)
    print(config.compute_config)

    cluster_manager = ClusterManager.from_dict(config.compute_config)
    cluster_manager.build_cluster()
    print(cluster_manager.cluster.scheduler_address)

if __name__ == '__main__':
    # test_compute_config()
    # test_pipe_config()
    # test_pipeline_config()
    test_remote_compute_config()
