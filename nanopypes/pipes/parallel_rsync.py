import time
from pathlib import Path
import os
import math

import pexpect
from dask.distributed import wait, Client, LocalCluster

from nanopypes.pipes.base import Pipe



class ParallelRsync(Pipe):

    def __init__(self, nchannels, local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):

        self.client = client
        self.local = Path(local_path)
        self.remote = Path(remote_path)
        self.password = password
        self.options = rsync_options
        self.direction = direction
        self.nchannels = nchannels

    def execute(self):
        if self.direction == 'push':
            src = self.local
            dest = self.remote

        elif self.direction == 'pull':
            src = self.remote
            dest = self.local

        data_per_call = math.ceil(len(os.listdir(str(src)))/self.nchannels)
        print(len(os.listdir(str(src))))
        print(data_per_call)
        all_futures = []
        data_to_send = ""
        data_counter = 0
        for data in os.listdir(str(src)):
            data_to_send += str(src.joinpath(data))
            data_to_send += " "
            data_counter += 1
            if data_counter == data_per_call:
                futures = self.client.submit(rsync, data_to_send, dest, self.password, self.options)
                #rsync(data_to_send, dest, self.password, self.options)
                all_futures.append(futures)
                data_counter = 0



        wait(all_futures)

def rsync(data, dest, password, options):

    # src = str(src.joinpath(data))
    dest = str(dest)
    args = ["-c", "rsync {} {} {}".format(options, data, dest)]
    print(args)
    child = pexpect.spawn('/bin/bash', args=args)
    #print(child.readline())
    time.sleep(2)
    i = child.expect(".*")
    print(i)
    child.sendline(password)
    child.expect(pexpect.EOF)
    child.close()

    return
#
# if __name__ == '__main__':
#     cluster = LocalCluster()
#     client = Client(cluster)
#     pr = ParallelRsync(nchannels=4, local_path='/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_01_remote/fast5/pass',
#                        remote_path='kf78w@ghpcc06.umassrc.org:/home/kf78w/test', password='k_Ww!xX?yUmass', client=client)
#     pr()
