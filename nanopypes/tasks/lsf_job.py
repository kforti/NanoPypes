import tempfile
import subprocess
import os
from pathlib import Path

from nanopypes.utilities import defaults_from_attrs


class LSFJob:
    def __init__(self, script_name=None, cores=None, mem=None, queue=None,
                 walltime=None, commands=None, job_name=None, shell=None,
                 out=None, err=None, save_path=None, script_path=None, exists=False):
        self.script_name = script_name
        self.cores = cores
        self.mem = mem
        self.queue = queue
        self.walltime = walltime
        self.commands = commands
        self.job_name = job_name
        self.shell = shell
        self.out = out
        self.err = err
        self.save_path = save_path
        self.job_script_path = script_path

        if exists and self.job_script_path is None:
            raise IOError("If the script exists you must also provide the script_path")
        elif exists:
            self._job_script = self._read_job_script(self._job_script)
        else:
            self.job_script = self.create_job_script()

    @defaults_from_attrs('job_script_path')
    def run(self, job_script_path=None, *dependencies):
        command = "bsub < {script_path}".format(script_path=job_script_path)
        current_env = os.environ.copy()
        with tempfile.NamedTemporaryFile(prefix="nanopypes-") as tmp:
            tmp.write(command.encode())
            tmp.flush()
            try:
                out = subprocess.check_output(
                    [self.shell, tmp.name], stderr=subprocess.STDOUT, env=current_env
                )
            except subprocess.CalledProcessError as exc:
                msg = "Command failed with exit code {0}: {1}".format(
                    exc.returncode, exc.output
                )
                pass  # TODO add logging
        return out

    @classmethod
    def from_dict(cls, dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(dict)
        instance.create_job_script()
        return instance

    @property
    def job_script(self):
        if self._job_script is None:
            self._job_script = self.create_job_script()
        return self._job_script

    def create_job_script(self):
        job_script = ["#!/bin/bash"]
        try:
            job_script.append('#BSUB -J {}'.format(self.job_name))
        except AttributeError:
            pass
        try:
            job_script.append('#BSUB -n {}'.format(self.cores))
            job_script.append('#BSUB -R "rusage[mem={}]"'.format(self.mem))
            job_script.append('#BSUB -W {}'.format(self.walltime))
            job_script.append('#BSUB -q {}'.format(self.queue))
            job_script.append('#BSUB -R "span[hosts=1]"')
        except:
            raise AttributeError("You must provide 'cores', 'mem', 'walltime', and 'queue' in order to create a job")

        try:
            job_script.append('#BSUB -L {}'.format(self.shell))
        except AttributeError:
            pass
        try:
            job_script.append('#BSUB -o {}'.format(self.out))
        except AttributeError:
            pass
        try:
            job_script.append('#BSUB -e {}'.format(self.err))
        except AttributeError:
            pass

        job_script.append("\n")
        job_script.extend(self.commands)
        return job_script

    def write_job_script(self, path=None):
        if path is None and self.save_path:
            path = Path(self.save_path).joinpath(self.script_name)
        elif path:
            pass
        elif path is None and self.save_path is None:
            raise IOError("No script save path provided")

        with open(str(path), 'w') as file:
            for line in self._job_script:
                file.write(line)
                file.write("\n")
        file.close()

    def _read_job_script(self, path):
        with open(path, 'r') as file:
            job_script = file.readlines()
        file.close()
        return job_script

