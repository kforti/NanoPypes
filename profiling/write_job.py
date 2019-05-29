from pathlib import Path
import subprocess

import nanopypes

#local_save_path = Path("/Users/kevinfortier/PycharmProjects/code_snippets/test_job_scripts")
#save_path = Path('/project/umw_athma_pai/kevin/data/Albacore_tests/')




class HPCJob:
    def __init__(self, script_name, cores, mem, queue, walltime, commands,
                 job_name=None, shell=None, out=None, err=None, save_path=None):
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
        self.create_job_script()

    @classmethod
    def from_dict(cls, dict):
        instance = cls.__new__(cls)
        instance.__dict__.update(dict)
        instance.create_job_script()
        return instance

    @property
    def job_script(self):
        return self._job_script

    def create_job_script(self):
        job_script = ["#!/bin/bash"]
        try:
            job_script.append('#BSUB -J {}'.format(self.job_name))
        except AttributeError:
            pass
        job_script.append('#BSUB -n {}'.format(self.cores))
        job_script.append('#BSUB -R "rusage[mem={}]"'.format(self.mem))
        job_script.append('#BSUB -W {}'.format(self.walltime))
        job_script.append('#BSUB -q {}'.format(self.queue))
        job_script.append('#BSUB -R "span[hosts=1]"')
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
        #job_cmd = 'read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fastq -r --save_path {save_path} --worker_threads {jthreads} --input /project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test --reads_per_fastq_batch 1000'.format(jthreads=threads, save_path=save_path)
        job_script.extend(self.commands)

        self._job_script = job_script

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


class HPCJobComponent(HPCJob):
    def __init__(self, script_name, cores, mem, queue, walltime, commands,
                 job_name=None, shell=None, out=None, err=None, save_path=None, script_path=None):
        super().__init__(script_name, cores, mem, queue, walltime, commands, job_name, shell, out, err, save_path)



    def job_submission(self, script_path):
        cmd = "bsub < {script_path}".format(script_path=script_path)
        process = subprocess.run(cmd, shell=True, check=True)
        return

    def __call__(self):
        save_path = str(Path(self.save_path).joinpath(self.script_name))
        self.job_submission(save_path)



if __name__ == '__main__':
    import yaml
    with open('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/profiling/profile_params', 'r') as yml:
        config = yaml.safe_load(yml)
    print(config)
    config = config["profile_runs"]["profile_run1"]["component2"]["job_script"]
    commands = ["echo hello world"]
    config["commands"] = commands
    my_job = HPCJob.from_dict(config)
    my_job.create_job_script()
    print(my_job.job_script)

    # names = []
    # fname = "albacore_test{num}.sh"
    # for i in range(6):
    #     names.append(fname.format(num=str(i+1)))
    # cores_list = [5, 10, 20, 30, 40, 50]
    # mem_list = [i*2048 for i in cores_list]
    # threads_list = cores_list
    # save_paths = [save_path.joinpath(i) for i in names]
    # local_save_paths = [local_save_path.joinpath(i) for i in names]
    # for i in range(6):
    #     write_job(names[i], cores_list[i], mem_list[i], threads_list[i], save_paths[i], local_save_paths[i])
    #     print(names[i], "\n", cores_list[i], "\n", mem_list[i], "\n", threads_list[i], "\n", save_paths[i])
