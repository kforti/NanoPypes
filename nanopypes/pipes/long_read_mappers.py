
from nanopypes.pipes.base import Pipe



class MiniMap(Pipe):
    commands = {'genomic': 'minimap2 -ax map-ont %(ref)s %(read)s -o %(output)s',
                'splice': 'minimap2 -ax splice %(ref)s %(read)s > %(output)s',
                'rna': 'minimap2 -ax splice -uf -k14 %(ref)s %(read)s -o %(output)s',
                'overlap': 'minimap2 -x ava-ont %(ref)s %(read)s -o %(output)s'}

    def __init__(self, input_paths, reference, save_path,
                 command_config, commands, pipeline):
        self.reference = reference
        self.save_path = save_path
        self.input = input_paths
        self.command_config = command_config
        self.commands = commands
        self.pipeline = pipeline



