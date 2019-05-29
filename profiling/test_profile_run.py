from pathlib import Path
import os

from profile_runs2 import ProfileRun




def test_write_job_script():
    job_script_path = Path("test_job_scripts/test_run1.sh")
    if job_script_path.exists():
        os.remove(str(job_script_path))
    pr = ProfileRun("test_run1", config_path='test_profile_params')

    assert job_script_path.exists()

def test_profile_run():
    pr = ProfileRun("test_run1", config_path='test_profile_params')
    pr()



if __name__ == '__main__':
    test_write_job_script()
    test_profile_run()
