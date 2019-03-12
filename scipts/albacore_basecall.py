from nanopypes.tools import basecall

if __name__ == '__main__':
    config = 'albacore_basecall.yml'
    bc_data = basecall(config, data_splits=400)


