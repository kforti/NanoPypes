import os
import shutil
import math
from pathlib import Path
from nanopypes.objects.basecalled import BaseCalledData, Summary, Telemetry, Configuration, PipelineLog, Workspace


def split_data(data_path, save_path, splits, compute=None, recursive=False):
    """Splits data into multiple directories for parallel processing"""
    data_path = Path(data_path)
    save_path = Path(save_path).joinpath("split_data")
    if save_path.exists() == False:
        save_path.mkdir()
    files = [data_path.joinpath(file) for file in os.listdir(str(data_path))]
    chunk_size = math.ceil((len(files) / splits))
    file_chunks = list(_chunks(files, chunk_size, save_path))

    if compute:
        print("Computing.........\n", _create_dir, "\n", file_chunks)
        compute.map(_create_dir, file_chunks)
        compute.show_progress()

    else:
        for files in file_chunks:
            _create_dir(files)


def _chunks(file_names, chunk_size, save_path):
    """Yield successive n-sized chunks from l."""
    counter = 0
    for i in range(0, len(file_names), chunk_size):
        new_dir_path = save_path.joinpath(str(counter))

        yield (new_dir_path, file_names[i:i + chunk_size])
        counter += 1

def _create_dir(files):
    print("Look HERE!!!!", files[0], files[0].exists())
    if files[0].exists() == False:
        files[0].mkdir()

    for file in files[1]:
        new_file_path = files[0].joinpath(file.name)
        shutil.copyfile(str(file), str(new_file_path))


def temp_dirs(data_dir, temp_location, parallel=True):
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
    num_splits = int(dir_len / 10)

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
    save_path = Path(save_path)
    batches = os.listdir(str(save_path))

    pipeline = PipelineLog(save_path.joinpath("pipeline.log"))
    seq_sum = Summary(save_path.joinpath("sequencing_summary.txt"))
    seq_tel = Telemetry(save_path.joinpath("sequencing_telemetry.js"))
    config = Configuration(save_path.joinpath("configuration.cfg"))
    workspace = Workspace(save_path.joinpath("workspace"))

    for batch in batches:
        batch_path = save_path.joinpath(batch)

        for temp in os.listdir(str(batch_path)):
            temp_path = batch_path.joinpath(temp)

            config.consume(src=temp_path.joinpath("configuration.cfg"))
            pipeline.consume(src=temp_path.joinpath("pipeline.log"))
            seq_sum.consume(src=temp_path.joinpath("sequencing_summary.txt"))
            seq_tel.consume(src=temp_path.joinpath("sequencing_telemetry.js"))
            workspace.consume(src=temp_path.joinpath("workspace"))

    config.combine()
    pipeline.combine()
    seq_tel.combine()
    seq_sum.combine()

    return BaseCalledData(path=save_path,
                          config=config,
                          pipeline=pipeline,
                          summary=seq_sum,
                          telemetry=seq_tel,
                          workspace=workspace)

