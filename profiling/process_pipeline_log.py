import argparse
import re
import time
from pathlib import Path

import pandas as pd


def get_batches(pipeline_data):
    time_pat = r'[0-9\-:,]+\s[0-9\-:,]+'
    sub_pat = r'Submitting file \".+\"'
    fin_pat = r'Finished\sprocessing\sfile\s\".+\"'
    read_pat = r'\".+\"'
    done_pat = r'\sDone.$'
    times = []
    data = {}  # read_name: {'submit': time,
    # 'finished': time }
    batches = []

    for p in pipeline_data:
        time = re.match(time_pat, p).group()
        time.replace(",", ":")
        submit = re.findall(sub_pat, p)
        finished = re.findall(fin_pat, p)
        done = re.findall(done_pat, p)
        if done:
            batches.append(data)
            data = {}
        elif submit:
            read = re.findall(read_pat, submit[0])
            read = read[0].replace('"', '')
            if read not in data:
                data[read] = {'submitted': None, 'finished': None}
            data[read]['submitted'] = time
        elif finished:
            read = re.findall(read_pat, finished[0])
            read = read[0].replace('"', '')
            if read not in data:
                data[read] = {'submitted': None, 'finished': None}
            data[read]['finished'] = time
    return batches


def get_df(batches):
    read_names = []#np.array(shape=len(data))
    submitted = []#np.array(shape=len(data))
    finished = []#np.array(shape=len(data))
    count = 0
    for batch in batches:
        for key, value in batch.items():
            read_names.append(key)
            submitted.append(value['submitted'])
            finished.append(value['finished'])
            count += 1

    df = pd.DataFrame({'read_name': read_names, 'submitted': pd.to_datetime(submitted), 'finished': pd.to_datetime(finished)})
    return df

def process_pipe(path):
    with open(path, 'r') as file:
        pipeline = file.readlines()
    batches = get_batches(pipeline)
    df = get_df(batches)

    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process pipeline.log")
    parser.add_argument("-p", nargs="+")
    args = parser.parse_args()
    paths = args.p
    #paths = ["/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_test/pipeline.log"]
    for p in paths:
        df = process_pipe(p)
        # print(df.head)
        # print(data)
        # print((df.finished-df.submitted).astype('timedelta64[ms]'))
        df["time_per_read"] = (df.finished-df.submitted).astype('timedelta64[s]')
        print(min(df.submitted))
        print(max(df.submitted))
        print((max(df.submitted)-min(df.submitted)))
        print(df["time_per_read"].mean())
        df.to_csv(str(Path(p).parent.name))
