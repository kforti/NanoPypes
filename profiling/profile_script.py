from paths import PATHS
from pathlib import PosixPath, Path
import shutil

from profile_runs import ProfileRun


def move_files(paths, save):
    for p in paths:
        if Path(p).exists():
            shutil.move(str(p), str(save))

if __name__ == '__main__':
    input_data_path = "/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass"
    new_dir = Path(input_data_path).joinpath("albacore_profile")
    if new_dir.exists() is False:
        new_dir.mkdir()

    runs = ["run2"]

    for key, value in PATHS.items():
        if key not in runs:
            continue
        move_files(value, new_dir)
        config = "profile_params"
        pr = ProfileRun(name=key, config_path=config)
        pr.run()



    # replace_with = "/project/umw_athma_pai/raw/minion/"
    # replace = "/project/umw_athma_pai/kevin/data/minion_ercc_labeled/"
    # path_dict = {}
    # for key, value in PATHS.items():
    #     paths = []
    #     for path in value:
    #         paths.append(str(path).replace(replace, replace_with))
    #     path_dict[key] = paths
    # print(path_dict)

