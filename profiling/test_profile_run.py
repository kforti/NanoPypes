from pathlib import Path
import os
import shutil

from profile_runs2 import ProfileRun




def test_write_job_script():
    job_script_path = Path("test_job_scripts/test_run1.sh")
    if job_script_path.exists():
        os.remove(str(job_script_path))
    pr = ProfileRun("test_run1", config_path='test_profile_params')

    assert job_script_path.exists()

def test_profile_run():
    pr = ProfileRun("test_run1", config_path='test_profile_params')
    pr.run()


def check_save_locations():
    comp1 = "/home/kf78w/bin/NanoPypes/tests/test_data/basecalled_data/results/profile_test/comp1"
    comp2 = "/home/kf78w/bin/NanoPypes/tests/test_data/basecalled_data/results/profile_test/comp2"
    comp1_contents = os.listdir(comp1)
    comp2_contents = os.listdir(comp2)
    if len(comp1_contents) > 0:
        remove_contents(comp1)
    if len(comp2_contents) > 0:
        remove_contents(comp2)

def remove_contents(path):
    shutil.rmtree(path)
    os.mkdir(path)
    return


if __name__ == '__main__':
    test_write_job_script()
    test_profile_run()
