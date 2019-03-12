from nanopypes.oxnano import *

config = Configuration("path/to/yaml/config")
compute_configs = config.compute
albacore = Albacore(compute_configs[compute_index])
