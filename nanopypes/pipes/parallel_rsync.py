import time
from pathlib import Path
import os

import pexpect
from dask.distributed import LocalCluster, Client, wait

from nanopypes.pipes.base import Pipe



class ParallelRsync(Pipe):

    def __init__(self, local_path, remote_path, password, rsync_options='-vcr', direction='push',  client='local'):

        self.client = client
        self.local = Path(local_path)
        self.remote = Path(remote_path)
        self.password = password
        self.options = rsync_options
        self.direction = direction

    def execute(self):
        if self.direction == 'push':
            src = self.local
            dest = self.remote

        elif self.direction == 'pull':
            raise NotImplementedError

        throttle_max = 5
        throttle = 0
        all_futures = []
        for data in os.listdir(str(src)):
            futures = self.client.submit(rsync, data, src, dest, self.password, self.options)
            all_futures.append(futures)
            throttle += 1
            if throttle == throttle_max:
                wait(all_futures)
                throttle = 0


        wait(all_futures)

def rsync(data, src, dest, password, options):

    src = str(src.joinpath(data))
    dest = str(dest)
    args = ["-c", "rsync {} {} {}".format(options, src, dest)]
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

