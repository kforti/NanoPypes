from prefect.tasks.shell import ShellTask


class AlbacoreBasecaller:

    def __init__(self, input_path=None, flowcell=None, kit=None, save_path=None,
                 output_format=None, reads_per_fastq=None, **kwargs):
        super().__init__(**kwargs)
        self.input_path = input_path
        self.flowcell = flowcell
        self.kit = kit
        self.save_path = save_path
        self.output_format = output_format
        self.reads_per_fastq = reads_per_fastq




