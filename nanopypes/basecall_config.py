BASECALLER_CONFIG = {
    ##fast5 raw data
    'input_path': '/project/umw_athma_pai/kevin/lambda_fast5/pass',#'/project/umw_athma_pai/kevin/data/pass', #'./test_data',

    ##albacore
    'save_path': '/project/umw_athma_pai/kevin/data/results', #'./save_data',
    'flowcell': 'FLO-MIN106',
    'kit' : 'SQK-LSK109',
    'barcoding': True,
    'output_format': 'fast5',
    'worker_threads': 1,
    'recursive': False,

    ##ghpcc cluster
    'job_time': '05:00',
    'mem': 2048,
    'ncpus': 1,
    'project': '/project/umw_athma_pai',
    'queue': 'long',

    ##dask
    'workers': 100,
    'cores': 1,
    'memory': '2 GB'
}
