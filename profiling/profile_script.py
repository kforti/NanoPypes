from paths import PATHS
from pathlib import Path
import shutil
import argparse
import os

from profile_runs import ProfileRun


def move_files(paths, save):
    for p in paths:
        if p.exists():
            shutil.move(str(p), str(save))

if __name__ == '__main__':
    input_data_path = Path("/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass")

    parser = argparse.ArgumentParser(description='Profile Run.')
    parser.add_argument("--run")
    parser.add_argument("--component", nargs='+', default=None)
    parser.add_argument("--num_batches", type=int)
    args = parser.parse_args()
    run = args.run
    comp = args.component
    num_batches = args.num_batches

    print("run: ", run)
    print("components: ", comp)
    print("num_batches: ", num_batches)

    new_dir = input_data_path.joinpath("albacore_profile_{}".format(run))
    if new_dir.exists() is False:
        new_dir.mkdir()
        batches = [input_data_path.joinpath(batch) for batch in os.listdir(str(input_data_path))[0:num_batches]]
    print(len(batches), batches)


    move_files(batches, new_dir)
    config = "profile_params"
    pr = ProfileRun(name=run, component=comp, config_path=config)
    pr.run()


