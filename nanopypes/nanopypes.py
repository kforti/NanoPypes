from nanopypes.objects import SeqOutput
from pathlib import Path
from nanopypes.utils import temp_dirs, remove_temps, collapse_save

def basecall(albacore, cluster):
    """ function for running the albacore basecaller in parallel on a cluster.
    """
    cluster.connect()
    func = albacore.build_func()
    input_path = Path(albacore.input_path)
    temp_path = input_path.joinpath("temp")

    print("bins: ", albacore.bins)
    for bin in albacore.bins:
        dirs = temp_dirs(bin, albacore.input_path)
        commands = []
        for dir in dirs:
            commands.append(albacore.build_command(dir, bin.name))
        print("commands: ", commands)
        cluster.map(func, commands)
        cluster.show_progress()

        remove_temps(temp_path)
    collapse_save(albacore.save_path)


if __name__ == '__main__':
    pass
