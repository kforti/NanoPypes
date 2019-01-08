import os
import shutil
from pathlib import Path

def temp_dirs(dir, location):
    """ Create temp directories and divide input data into these directories"""
    path = Path(location)
    temp_path = path.joinpath('temp')
    temp_path.mkdir()
    dir_path = str(path.joinpath(dir))
    print(dir_path)
    dir_len = len(os.listdir(dir_path))
    num_splits = int(dir_len / 4)

    if dir_len % num_splits == 0:
        num_files = int(dir_len / num_splits)
    else:
        num_files = int(dir_len / num_splits) + 1

    dirs_list = []
    files = file_generator(dir_path)
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
            new_file_path = str(p.joinpath(file_name))
            shutil.copyfile(file_path, new_file_path)
            count += 1

        if len(os.listdir(str(p))) > 0:
            dirs_list.append(str(p))
    return dirs_list


def file_generator(dir):
    for file in os.listdir(dir):
        file_path = dir + '/' + file
        yield file_path

def dir_generator(dir):
    for dir in os.listdir(dir):
        if dir == 'temp':
            continue
        yield dir

def remove_temps(path):
    try:
        path = path + '/temp'
        shutil.rmtree(path)
    except Exception as e:
        print(e)

def copyfiles(src, destination):
    for file in os.listdir(src):
        if Path(src).joinpath(file).is_file():
            file_src = "/".join([src, file])
            file_dest = "/".join([destination, file])
            shutil.copyfile(file_src, file_dest)
        else:
            continue

# def create_temp_files(fast5, num_workers):
#     """Creates temporary directories and files for parallel basecalling"""
#     reads_per_dir = fast5.num_reads / num_workers
#     list_of_dirs = []
#
#     input_path = fast5.path
#     tmp_path = input_path.joinpath('temp')
#     os.mkdir(tmp_path)
#
#     for i in range(num_workers):
#         dir_name = str(i)
#         dir_path = tmp_path.joinpath(dir_name)
#         list_of_dirs.append(dir_path)
#         os.mkdir(dir_path)
#
#     reads_count = 0
#     workers_count = 0
#     for dir in os.listdir(input_path):
#         if dir == '.DS_Store' or dir == 'temp':
#             continue
#         curr_reads_dir = input_path.joinpath(dir)
#
#         for file in os.listdir(curr_reads_dir):
#             if file == '.DS_Store':
#                 continue
#             #print('hi')
#             old_path = input_path.joinpath(dir, file)
#             #print(old_path.name)
#             new_path = tmp_path.joinpath(str(workers_count), file)
#             #print(new_path.name)
#             copyfile(old_path, new_path)
#
#             reads_count += 1
#             if reads_count > reads_per_dir:
#                 reads_count = 0
#                 workers_count += 1