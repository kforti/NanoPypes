import time
from pathlib import Path
import os
import math

import pexpect
from dask.distributed import wait, Client, LocalCluster

from nanopypes.core.data_transform import DataTransform



class ParallelRsync(DataTransform):

    def __init__(self, nchannels, local_path, remote_path, password, rsync_options='-avr', direction='push',  client='local'):

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
