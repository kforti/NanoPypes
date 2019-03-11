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
MINION_SAMPLES = ["test_data/minion_sample_raw_data/Experiment_01/sample_01_remote",
                  "test_data/minion_sample_raw_data/Experiment_01/sample_02_local"]
#BASECALLED Data

# read = RawFast5("test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass/0/imac_ad_umassmed_edu_20181108_FAK30311_MN27234_sequencing_run_test_61366_read_102_ch_58_strand.fast5")
# read.contents
# data = read.get_raw_data()
# print(data)
data_path = Path("test_data/minion_sample_raw_data/Experiment_01/sample_02_local/0")
fast5_path = Path("test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5")
splits = 10
num_files = 20

def file_generator(data_path):
    for file in os.listdir(data_path):
        yield data_path.joinpath(file)

def create_data_dir(data_path, fast5_path, splits, num_files):
    files = file_generator(data_path)
    p = fast5_path.joinpath("pass")
    p.mkdir()
    f = fast5_path.joinpath("fail")
    f.mkdir()

    for i in range(splits):
        pd = p.joinpath(str(i))
        pd.mkdir()
        fd = f.joinpath(str(i))
        fd.mkdir()
        counter = 0
        while counter < num_files:
            pfile = next(files)
            ffile = next(files)
            shutil.move(str(pfile), str(pd))
            shutil.move(str(ffile), str(fd))
            counter += 1

# create_data_dir(data_path=data_path,
#                 fast5_path=fast5_path,
#                 splits=splits,
#                 num_files=num_files)
# bc_data = RawFast5("test_data/basecalled_data/results/local_basecall_test/0/0/workspace/pass/0/imac_ad_umassmed_edu_20181108_FAK30311_MN27234_sequencing_run_test_61366_read_26_ch_182_strand.fast5")
# bc_data.contents
# fastq = bc_data.get_fastq()
# print(fastq)



basecalled_data_path = Path("test_data/basecalled_data/utils_tests/local_basecall_test")
collapse_path = Path("test_data/basecalled_data/utils_tests/bc_copy")
shutil.copytree(str(basecalled_data_path), str(collapse_path))
results = ParallelBaseCalledData(collapse_path)
results.collapse_parallel_data(compute=self.compute)

