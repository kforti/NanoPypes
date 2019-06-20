from pathlib import Path
import os
import shutil

from profile_runs import ProfileRun




def test_write_job_script():
    job_script_path = Path("test_job_scripts/test_run1.sh")
    if job_script_path.exists():
        os.remove(str(job_script_path))
    pr = ProfileRun("test_run1", config_path='test_profile_params')

    assert job_script_path.exists()

def test_albacore_pipe_run():
    pr = ProfileRun("test_run1", config_path='test_profile_params')
    pr.run()


def check_save_locations():
    comp1 = "../tests/test_data/basecalled_data/results/profile_test/comp1"
    comp2 = "../tests/test_data/basecalled_data/results/profile_test/comp2"
    comp1_contents = os.listdir(comp1)
    comp2_contents = os.listdir(comp2)
    if len(comp1_contents) > 0:
        remove_contents(comp1)
    if len(comp2_contents) > 0:
        remove_contents(comp2)

    profile_run_data = "profile_run_data"
    if len(os.listdir(profile_run_data)) > 1:
        remove_contents(profile_run_data)

def remove_contents(path):
    shutil.rmtree(path)
    os.mkdir(path)
    return


def test_profile_run():
    check_save_locations()
    config = "test_profile_params"
    pr = ProfileRun(name="run1", config_path=config)
    pr.run()

if __name__ == '__main__':
    #test_write_job_script()
    test_profile_run()
