from pathlib import Path
from nanopypes.pipes import Pipe


class MiniMap2(Pipe):
    def __init__(self, fastq_path, reference, compute, save_path, function):
        self.compute = compute
        self.fastq_path = Path(fastq_path)
        self.fastq_paths = [str(self.fastq_path.joinpath(file)) for file in os.listdir(str(self.fastq_path))]
        self.reference = Path(reference)
        self.save_path = Path(save_path)

    @property
    def info(self):
        print("Fastq Paths: \n", self.fastq_paths)

    def execute(self):
        self.compute.map(self.func, ['a', 'b', 'c'])

        self.compute.close()

    def minimap_func(self):
        def mapper(fastq_path):
            fastq = Path(fastq_path)
            sam_file = self.save_path.joinpath((fastq.name.replace('.fq', '.sam')))
            command = ['minimap2', '-ax splice', str(self.reference), fastq, '>', sam_file]
            return command
            # process = subprocess.Popen(command)
            # process.wait()
        return mapper


