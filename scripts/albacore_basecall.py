<<<<<<< HEAD
from nanopypes.tools import basecall

if __name__ == '__main__':
    config = 'albacore_basecall.yml'
    bc_data = basecall(config,
                       continue_on=True,
                       last_batch=None,
                       data_splits=100)
=======
from nanopypes.run_pipes import albacore_basecaller

if __name__ == '__main__':
    config = 'albacore_basecall.yml'
    bc_data = albacore_basecaller(config,
                                  data_splits=125,
                                  batch_bunch=100)
>>>>>>> version1.0


