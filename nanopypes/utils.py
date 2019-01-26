import os
import shutil
import csv
from pathlib import Path
import json

def temp_dirs(data_dir, temp_location):
    """ Create temp directories and divide input data into these directories
    Return list of temp directory locations
    :Parameters:
    - 'data_dir': string name of the directory
    - 'temp_location': string relative path to where the temp directory is to be located
    """
    temp_location = Path(temp_location)
    data_dir = Path(data_dir)
    temp_path = temp_location.joinpath('temp')
    temp_path.mkdir()

    dir_len = len(os.listdir(str(data_dir)))
    num_splits = int(dir_len / 4)

    if dir_len % num_splits == 0:
        num_files = int(dir_len / num_splits)
    else:
        num_files = int(dir_len / num_splits) + 1

    dirs_list = []
    files = file_generator(data_dir)
    for i in range(num_splits):
        count = 0
        dir_name = str(i)
        p = temp_path.joinpath(dir_name)
        p.mkdir()
        while count < num_files:
            try:
                file_path = next(files)
            except Exception as e:
                print(e)
                break
            file_name = Path(file_path).name
            new_file_path = p.joinpath(file_name)
            shutil.copyfile(str(file_path), str(new_file_path))
            count += 1

        if len(os.listdir(str(p))) > 0:
            dirs_list.append(str(p))
    return dirs_list

def file_generator(dir):
    for file in os.listdir(str(dir)):
        file_path = dir.joinpath(file)
        yield file_path

def remove_temps(path):
    try:
        shutil.rmtree(str(path))
    except Exception as e:
        print(e)

def collapse_save(save_path):
    """ Collapse all the data into the expected output"""
    names = ["pass", "fail", "calibration_strands"]

    for i, bin in enumerate(os.listdir(str(save_path))):
        bin_path = save_path.joinpath(bin)
        if bin_path.is_file():
            continue

        for child in os.listdir(str(bin_path)):
            if child == "sequencing_summary.txt":
                sum_path = bin_path.joinpath(child)
                new_sum_path = save_path.joinpath(child)
                with open(str(sum_path), mode="r") as file:
                    csv_reader = csv.reader(file, delimiter="\t")
                    row_num = 0
                    for row in csv_reader:
                        if i != 0 and row_num == 0:
                            row_num += 1
                            continue
                        row_num += 1
                        with open(str(new_sum_path), mode="a") as sum_file:
                            csv_writer = csv.writer(sum_file, delimiter="\t")
                            csv_writer.writerow(row)

            elif child == "workspace":
                workspace_path = bin_path.joinpath(child)

            elif child == "sequencing_telemetry.js":
                with open(str(bin_path.joinpath(child)), "r") as file:
                    tel_data = json.load(file)
                with open(str(save_path.joinpath(child)), "a") as file:
                    json.dump(tel_data, file)

            elif i == 0 and child == "configuration.cfg":
                shutil.copy(str(bin_path.joinpath(child)), str(save_path.joinpath(child)))

            elif i == 0 and child == "pipeline.log":
                shutil.copy(str(bin_path.joinpath(child)), str(save_path.joinpath(child)))

        if i == 0:
            new_workspace = save_path.joinpath(workspace_path.name)
            os.mkdir(str(new_workspace))

            for name in names:
                path = new_workspace.joinpath(name)
                if not path.exists():
                    path.mkdir()

        cal_strands = workspace_path.joinpath("calibration_strands", "0")
        new_cal_strands = new_workspace.joinpath("calibration_strands", bin)
        if not new_cal_strands.exists():
            new_cal_strands.mkdir()

        pass_reads = workspace_path.joinpath("pass", "0")
        new_pass_reads = new_workspace.joinpath("pass", bin)
        if not new_pass_reads.exists():
            new_pass_reads.mkdir()

        fail_reads = workspace_path.joinpath("fail", "0")
        new_fail_reads = new_workspace.joinpath("fail", bin)
        if not new_fail_reads.exists():
            new_fail_reads.mkdir()

        dump_reads(cal_strands, new_cal_strands)
        dump_reads(pass_reads, new_pass_reads)
        dump_reads(fail_reads, new_fail_reads)

        shutil.rmtree(bin_path)
    return 0

def consolidate_summary(src, dest):
    pass

def consolidate_telemetry(src, dest):
    pass

def dump_reads(src, dest):
    for read in os.listdir(str(src)):
        shutil.copy(str(src.joinpath(read)), str(dest.joinpath(read)))
    return 0

