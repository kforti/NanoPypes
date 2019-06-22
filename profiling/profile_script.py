from paths import PATHS
from pathlib import PosixPath, Path
import shutil

from profile_runs import ProfileRun


def move_files(paths, save):
    for p in paths:
        if p.exists():
            shutil.move(str(p), str(save))

if __name__ == '__main__':
    input_data_path = "/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass"
    new_dir = Path(input_data_path).joinpath("albacore_profile")
    if new_dir.exists() is False:
        new_dir.mkdir()

    runs = ["run1", "run2"]

    for key, value in PATHS.items():
        if key not in runs:
            continue
        move_files(value, new_dir)
        config = "profile_params"
        pr = ProfileRun(name=key, config_path=config)
        pr.run()
