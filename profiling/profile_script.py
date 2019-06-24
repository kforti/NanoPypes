from paths import PATHS
from pathlib import PosixPath, Path
import shutil
import argparse

from profile_runs import ProfileRun


def move_files(paths, save):
    for p in paths:
        if Path(p).exists():
            shutil.move(str(p), str(save))

if __name__ == '__main__':
    input_data_path = Path("/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass")

    parser = argparse.ArgumentParser(description='Profile Run.')
    parser.add_argument("--run")
    parser.add_argument("--components", nargs='+', default=None)
    parser.add_argument("--num_batches")
    args = parser.parse_args()
    run = args.run
    comps = args.components
    num_batches = args.num_batches

    print("run: ", run)
    print("components: ", comps)
    print("num_batches: ", num_batches)
    import os
    new_dir = input_data_path.joinpath("albacore_profile_{}".format(run))
    batches = [input_data_path.joinpath(batch) for batch in os.listdir(str(input_data_path))[0:num_batches]]
    print(len(batches), batches)


    # new_dir = Path(input_data_path).joinpath("albacore_profile")
    # if new_dir.exists() is False:
    #     new_dir.mkdir()
    #
    # runs = ["run2"]
    #
    # for run in runs:
    #     move_files(PATHS[run], new_dir)
    #     config = "profile_params"
    #     pr = ProfileRun(name=run, config_path=config)
    #     pr.run()


