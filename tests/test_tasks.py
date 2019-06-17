import os

import pytest

from nanopypes.tasks import ShellTask, LSFJob, SingularityTask


def test_shell_task_command():
    command = "echo hello world"
    task = ShellTask(command)
    output = task.run()
    assert output == b"hello world\n"

def example_python_helper_script():
    import sys
    test_shell_task_command()
    st = ShellTask(command="sys.stdout.write(hi())", helper_script="import sys\ndef hi(): return 'hello world'",
                   shell='python3')
    out = st.run()
    print(out)

def test_lsf_job():
    expected_path = "test_lsf_script"
    lsf_job = LSFJob(script_name="test_lsf_script",
                     cores=8,
                     mem=2048,
                     queue="short",
                     walltime="01:30",
                     commands=["echo hello world", "ls"],
                     job_name="test_job",
                     out="test_job.out",
                     err="test_job.err",
                     save_path="."
                     )
    expected_output = ['#!/bin/bash',
                       '#BSUB -J test_job',
                       '#BSUB -n 8',
                      '#BSUB -R "rusage[mem=2048]"',
                      '#BSUB -W 01:30',
                      '#BSUB -q short',
                      '#BSUB -R "span[hosts=1]"',
                      '#BSUB -L bash',
                      '#BSUB -o test_job.out',
                      '#BSUB -e test_job.err',
                      'echo hello world',
                      'ls']

    lsf_job.write_job_script()
    with open(expected_path, 'r') as file:
        for line in file:
            if line == "\n":
                continue
            line = line.strip("\n")
            assert line in expected_output

    os.remove(expected_path)

if __name__ == '__main__':
    test_lsf_job()



