import pexpect
import os
import time

from dask.distributed import Client, LocalCluster


def rsync_parallel(local_path, remote_path, password, options, direction='push'):
    command = 'rsync '
    if direction == 'push':
        command += options
    if local_path[-1] != '/':
        local_path = local_path + '/'
    if remote_path[-1] != '/':
        remote_path = remote_path + '/'

    def rsync(data, command=command):

        src = local_path + data
        des = remote_path + data
        args = ["-c", "rsync {} {} {}".format(options, src, des)]
        print(args)
        child = pexpect.spawn('/bin/bash', args=args)
        # print(child.readline())
        time.sleep(1)
        i = child.expect("kf78w@ghpcc06.umassrc.org's password: ")
        print(i)
        child.sendline(password)
        child.expect(pexpect.EOF)
        child.close()
        return

    return rsync


if __name__ == '__main__':
    cluster = LocalCluster()
    client = Client(cluster)

    remote = 'kf78w@ghpcc06.umassrc.org:/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass'
    local = '/Users/kevinfortier/Desktop/NanoPypes/NanoPypes/pai-nanopypes/tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass'
    options = ['v', 'c', 'r']
    func = rsync_parallel(local, remote, 'k_Ww!xX?yUmass', '-vcr')

    data = os.listdir(local)

    futures = client.map(func, data)
    resp = client.gather(futures)
    for future in resp:
        print(future)
    client.close()







