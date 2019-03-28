from nanopypes.run_pipes import albacore_basecaller

if __name__ == '__main__':
    config = 'albacore_basecall.yml'
    bc_data = albacore_basecaller(config,
                                  data_splits=125,
                                  batch_bunch=100)


