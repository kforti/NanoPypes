import os
import shutil
from pathlib import Path
from nanopypes.objects.raw import RawFast5


#####################################################################
### Test Data Paths                                               ###
#####################################################################

#MINION Raw Data
MINION_SEQ_OUT = "test_data/minion_sample_raw_data"
MINION_EXPERIMENT = "test_data/minion_sample_raw_data/Experiment_01"
MINION_SAMPLES = {"remote": "test_data/minion_sample_raw_data/Experiment_01/sample_01_remote",
                  "local": "test_data/minion_sample_raw_data/Experiment_01/sample_02_local"]
#BASECALLED Data

