import os
import re
import pandas as pd
from Bio import SeqIO
from math import ceil

def get_log_data(dirpath):
    with open(os.path.join(dirpath, 'pipeline.log'), 'r') as file:
        pipeline = file.readlines()

        time_pat = r'[0-9\-:,]+\s[0-9\-:,]+'
        sub_pat = r'Submitting file \".+\"'
        fin_pat = r'Finished\sprocessing\sfile\s\".+\"'
        read_pat = r'\".+\"'
        read_num_pat = r'read_[0-9]+_ch_[0-9]+'
        done_pat = r'\sDone.$'
        times = []
        data = {}  # read_name: {'submit': time,
        # 'finished': time }

        batches = []

        for p in pipeline:
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
                read_chan = re.findall(read_num_pat, read)[0]
                # print(read_num)
                if read not in data:
                    data[read] = {'read_channel': read_chan}
                data[read]['submitted'] = time
            elif finished:
                read = re.findall(read_pat, finished[0])
                read = read[0].replace('"', '')
                read_num = re.findall(read_num_pat, read)[0]
                if read not in data:
                    data[read] = {}
                data[read]['finished'] = time
        read_names = []  # np.array(shape=len(data))
        submitted = []  # np.array(shape=len(data))
        finished = []  # np.array(shape=len(data))
        read_chans = []
        count = 0
        for batch in batches:
            for key, value in batch.items():
                read_names.append(key)
                submitted.append(value['submitted'])
                finished.append(value['finished'])
                read_chans.append(value['read_channel'])
                count += 1

        df = pd.DataFrame(
            {'read_name': read_names, 'read_channel': read_chans, 'submitted': pd.to_datetime(submitted), 'finished': pd.to_datetime(finished)})
        # print(df.head)
        # print(data)
        # print((df.finished-df.submitted).astype('timedelta64[ms]'))
        df["time_per_read"] = (df.finished - df.submitted).astype('timedelta64[ms]')

        return df


def get_fq_paths(dirpath):
    wpath = os.path.join(dirpath,'workspace')
    fqfolders = [os.path.join(wpath,i) for i in os.listdir(wpath)]
    fqs = []

    for folder in fqfolders:
        for file in os.listdir(folder):
            fqs.append(os.path.join(folder, file))

    return fqs


def dask_get_lens(fqlist):
    readnames = {}
    for path in fqlist:
        for rec in SeqIO.parse(open(path, 'r'), 'fastq'):
            try:
                readnames[rec.name] += len(rec)
            except KeyError:
                readnames[rec.name] = len(rec)

    df = pd.DataFrame({'read_name': list(readnames.keys()), 'read_len': list(readnames.values())})
    return df


def re_get_name(pathlist):
    readnames = {}
    read_num_pat = r'read=[0-9]+'
    ch_num_pat = r'ch=[0-9]+'
    for path in pathlist:
        for rec in SeqIO.parse(path, "fastq"):
            read_num = re.findall(read_num_pat, rec.description)
            read_num = read_num[0].replace("=", "_")
            ch_num = re.findall(ch_num_pat, rec.description)
            ch_num = ch_num[0].replace("=", "_")
            try:
                readnames["_".join([read_num, ch_num])] += len(rec)
            except KeyError:
                readnames["_".join([read_num, ch_num])] = len(rec)

    return pd.DataFrame({'read_channel': list(readnames.keys()), 'read_len': list(readnames.values())})


def gen_df(pathlist):
    biglogdf = pd.DataFrame()
    bigfqdf = pd.DataFrame()
    for dirpath in pathlist:
        ls1 = [biglogdf, get_log_data(dirpath)]
        biglogdf = pd.concat(ls1)
        fqlist = get_fq_paths(dirpath)
        ls2 = [bigfqdf, re_get_name(fqlist)]
        bigfqdf = pd.concat(ls2)

    return pd.merge(bigfqdf, biglogdf, on='read_channel', how='right')

    # print('merged:', finaldf.shape)
    # print('log:', biglogdf.shape)
    # print('fq:', bigfqdf.shape)
    # print(finaldf.head())

def run_funcs(path, client, workers):
    # path = '/Users/parkersimpson/PycharmProjects/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_copy'
    dirlist = [os.path.join(path, i) for i in os.listdir(path)]
    map_list = []
    partitions = ceil(len(dirlist) / workers)
    # mod = len(dirlist) % 50
    for i in range(0, len(dirlist), partitions):
        map_list.append(dirlist[i:i + partitions])

    futures = client.map(gen_df, map_list)
    big_Df = pd.concat(client.gather(futures))
    #print(big_Df.shape, big_Df.head)
    return big_Df


if __name__ == '__main__':
    from distributed import Client

    client = Client()

    path = "../tests/test_data/basecalled_data/results/local_basecall_copy"
    df = run_funcs(path, client, workers=4)
    df.drop_duplicates()
    print(df.submitted.min())
    print(df.finished.max())
    runtime = df.finished.max() - df.submitted.min()
    print(runtime)
    print(df.time_per_read.sum())
    print("SHAPE: ", df.shape)
    print(df.read_len.sum()/runtime.total_seconds())
    #df["time"] = df["date"].astype("datetime64")
    submitted_df = pd.DataFrame({"submitted": df.submitted, "time_per_read": df.time_per_read})
    print(submitted_df.head())
    plot = submitted_df.plot(kind="bar", x="submitted", y="time_per_read")
    fig = plot.get_figure()
    fig.savefig("./submitted_hist.png")
    finished_df = pd.DataFrame({"finished": df.finished, "time_per_read": df.time_per_read})
    plot = finished_df.plot(kind="bar", x="finished", y="time_per_read")
    fig = plot.get_figure()
    fig.savefig("./finished_hist.png")

    plot = df.plot(kind="bar", x="read_len", y="time_per_read")
    fig = plot.get_figure()
    fig.savefig("./time_v_length.png")



    # plot = df.groupby(df.finished.dt.minute).count().plot(kind="bar")
    # fig = plot.get_figure()
    # fig.savefig("./finished_hist.png")
    # plot = df.groupby(df.time_per_read/1000).count().plot(kind="bar")
    # fig = plot.get_figure()
    # fig.savefig("./time_per_read.png")


