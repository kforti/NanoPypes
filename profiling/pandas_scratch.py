import pandas as pd
import numpy as np

import re


with open('/Users/kevinfortier/Desktop/NanoPypes_Prod/NanoPypes/tests/test_data/basecalled_data/results/local_basecall_test/pipeline.log', 'r') as file:
    pipeline = file.readlines()

time_pat = r'[0-9\-:,]+\s[0-9\-:,]+'
sub_pat = r'Submitting file \".+\"'
fin_pat = r'Finished\sprocessing\sfile\s\".+\"'
read_pat = r'\".+\"'
done_pat = r'\sDone.$'
times = []
data = {} #read_name: {'submit': time,
                      #'finished': time }

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
        if read not in data:
            data[read] = {}
        data[read]['submitted'] = time
    elif finished:
        read = re.findall(read_pat, finished[0])
        read = read[0].replace('"', '')
        if read not in data:
            data[read] = {}
        data[read]['finished'] = time
print(batches)
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
# print(df.head)
# print(data)
# print((df.finished-df.submitted).astype('timedelta64[ms]'))
df["time_per_read"] = (df.finished-df.submitted).astype('timedelta64[s]')
print(min(df.submitted))
print(max(df.submitted))
print((max(df.submitted)-min(df.submitted)))
print(df["time_per_read"].mean())
