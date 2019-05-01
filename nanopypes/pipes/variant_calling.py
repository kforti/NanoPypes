from nanopypes.pipes.base import Pipe

from pathlib import Path
import subprocess
import os

from distributed import wait


class VariantCalling(Pipe):
    commands = {'sam_to_bam': 'samtools view -b -S -o %(bam)s %(sam)s',
                'sort_bam': 'samtools sort %(bam)s -o %(sorted_bam)s',
                'index': 'samtools index %(sorted_bam)s %(bam_index)s',
                'bcftools_mpileup': 'bcftools mpileup -Ob -f %(ref)s %(sorted_bam)s > %(bcf)s',
                'bcftools_call': 'bcftools call -c -v %(bcf)s > %(vcf)s'}
    args_pattern = {'bam': '',
                    'sam': '',
                    'ref': '',
                    'bcf': '',
                    'vcf': '',
                    'sorted_bam': '',
                    'bam_index': ''}

    def __init__(self, input_path, reference, client, save_path, input_type='sam'):
        self.client = client
        self.reference = Path(reference)
        self.save_path = Path(save_path)
        self.input = Path(input_path)
        self.input_type = input_type

        self.futures = []

    def execute(self):
        for file in os.listdir(str(self.input)):
            dependencies = []
            if self.input_type == 'sam':
                #Convert Bam to Sam
                bam_file = self.save_path.joinpath(file.replace('.sam', '.bam'))
                sb_args = {'sam': str(self.input.joinpath(file)),
                           'bam': str(bam_file)}
                sam_to_bam_command = self.commands['sam_to_bam'] % sb_args
                sam_to_bam = self.client.submit(run_subprocess, sam_to_bam_command)
                dependencies.append(sam_to_bam)
            else:
                bam_file = self.input.joinpath(file)

            #Sort Bam
            sorted_bam_file = self.save_path.joinpath(bam_file.name.replace('.bam', '.sorted.bam'))
            sorted_bam_args = {'bam': str(bam_file),
                               'sorted_bam': str(sorted_bam_file)}
            sort_bam_command = self.commands['sort_bam'] % sorted_bam_args
            sort_bam = self.client.submit(run_subprocess, sort_bam_command, dependencies)
            dependencies.append(sort_bam)

            #Index Bam
            index_bam_file = self.save_path.joinpath((bam_file.name + '.bai'))
            index_bam_args = {'sorted_bam': str(sorted_bam_file),
                              'bam_index': str(index_bam_file)}
            index_bam_command = self.commands['index'] % index_bam_args
            index_bam = self.client.submit(run_subprocess, index_bam_command, dependencies)
            dependencies.append(index_bam)

            #Pileup
            bcf_file = self.save_path.joinpath(bam_file.name.replace('.bam', '.bcf'))
            bcf_args = {'ref': self.reference,
                        'sorted_bam': str(sorted_bam_file),
                        'bcf': str(bcf_file)}
            bcf_mpileup_command = self.commands['bcftools_mpileup'] % bcf_args
            bcf_mpileup = self.client.submit(run_subprocess, bcf_mpileup_command, dependencies)
            dependencies.append(bcf_mpileup)

            # Variant Calling
            vcf_file = self.save_path.joinpath(bam_file.name.replace('.bam', '.vcf'))
            call_args = {'bcf': str(bcf_file),
                        'vcf': str(vcf_file)}
            bcf_call_command = self.commands['bcftools_call'] % call_args
            bcf_call = self.client.submit(run_subprocess, bcf_call_command, dependencies)
            dependencies.append(bcf_call)
            self.futures.append(dependencies)

        wait(self.futures)
        for f in self.futures:
            for i in f:
                print(i.result())
        return


def run_subprocess(command, dependencies=None):
    process = subprocess.run(command, shell=True)
    return process.stdout, process.stderr

    #return command

if __name__ == '__main__':
    from distributed import LocalCluster, Client
    cluster = LocalCluster()
    client = Client(cluster)
    v = VariantCalling(input_path='../../tests/test_data/minimap/sam_files', reference='../../tests/test_data/minimap/references/Plasmodium_falciparum_3D7.fasta',
                       client=client, save_path='../../tests/test_data/minimap/variant_calling_output', input_type='sam')
    v()
