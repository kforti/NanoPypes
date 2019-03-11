from nanopypes.objects.basecalled import *
from nanopypes.objects.raw import *
from pathlib import Path
import unittest


paths = [Path('test_data/basecalled_data/Experiment_01/sample_01_remote/workspace/calibration_strands'),
         Path('test_data/basecalled_data/Experiment_01/sample_01_remote/workspace/pass'),
         Path('test_data/basecalled_data/Experiment_01/sample_01_remote/workspace/fail'),
         Path('test_data/basecalled_data/Experiment_01/sample_02_local/workspace/calibration_strands'),
         Path('test_data/basecalled_data/Experiment_01/sample_02_local/workspace/pass'),
         Path('test_data/basecalled_data/Experiment_01/sample_02_local/workspace/fail')]

def generate_barcodes(paths):
    for path in paths:
        path.joinpath('Unclassified').mkdir()
        for i in range(10):
            path.joinpath(str(i)).mkdir()

class TestRaw(unittest.TestCase):
    """Tests for the Albacore class."""


    def setUp(self):
        """Set up test fixtures, if any."""


    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_sample(self):
        data = SeqOutput('test_data/minion_sample_raw_data')
        sample = data.get_sample('Experiment_01', 'sample_01_remote')
        num_reads = sample.num_reads
        self.assertTrue(num_reads['pass'] == 840)
        self.assertTrue(num_reads['fail'] == 840)


class TestBasecalled(unittest.TestCase):
    """Tests for the Albacore class."""


    def setUp(self):
        """Set up test fixtures, if any."""


    def tearDown(self):
        """Tear down test fixtures, if any."""

    # def test_001_BaseCalledReadBarcodes(self):
    #     path = 'test_data/basecalled_data/Experiment_01/sample_01_remote/workspace/pass'
    #     read_barcodes = BaseCalledReadBarcodes(path)
    #     print(read_barcodes.barcodes)
    #     print(read_barcodes.num_barcodes)
    #
    # def test_001_BaseCalledRead(self):
    #     path = 'test_data/basecalled_data/results/0/workspace/pass/0/imac_ad_umassmed_edu_20181108_FAK30311_MN27234_sequencing_run_test_61366_read_102_ch_58_strand.fast5'
    #     bc_read = BasecalledRead(path, 'imac_ad_umassmed_edu_20181108_FAK30311_MN27234_sequencing_run_test_61366_read_102_ch_58_strand')
    #     bc_read.contents
