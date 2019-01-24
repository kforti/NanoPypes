from nanopypes.objects import SeqOutput
from pathlib import Path
from nanopypes.utils import temp_dirs, remove_temps, collapse_save

def basecall(albacore, cluster):
    """ function for running the albacore basecaller in parallel on a cluster.
    """
    cluster.connect_workers()
    func = albacore.build_func()
    input_path = Path(albacore.input_path)
    temp_path = input_path.joinpath("temp")

    for bin in albacore.bins:
        dirs = temp_dirs(bin, albacore.input_path)
        commands = []
        for dir in dirs:
            commands.append(albacore.build_command(dir, bin.name))
        cluster.map(func, commands)

        remove_temps(temp_path)
    collapse_save(albacore.save_path)


if __name__ == '__main__':
    pass
