from nanopypes.tools import basecall

if __name__ == '__main__':
    config = 'albacore_basecall.yml'
    bc_data = basecall(config,
                       continue_on=True,
                       last_batch=None,
                       data_splits=100)


