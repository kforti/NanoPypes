import subprocess
import argparse
import os
import time

import pexpect
import dotenv

dotenv.load_dotenv("env/.env")
LSF_PASSWORD = os.environ['LSF_PASSWORD']
SLURM_PASSWORD = os.environ['SLURM_PASSWORD']
SSH_PASSWORD = os.environ['SSH_PASSWORD']


parser = argparse.ArgumentParser(description='Push code to cluster.')
parser.add_argument("-m")
parser.add_argument("-b")
parser.add_argument("-c")
args = parser.parse_args()
msg = args.m
branch = args.b
cluster = args.c

subprocess.call(["git", "add", "--all"])
subprocess.call(["git", "commit", "-m", msg])
subprocess.call(["git", "push", "origin", branch])

if cluster == "lsf":
    child = pexpect.spawn("ssh kf78w@ghpcc06.umassrc.org")
    r = child.expect("password:")
    child.sendline(LSF_PASSWORD)
    child.expect("git 2.9.5 is located under")
elif cluster == 'slurm':
    child = pexpect.spawn("ssh -F /Users/kevinfortier/c3ddb-cluster/linux/config c3ddb01.mit.edu")
    r = child.expect("Enter passphrase for key '/Users/kevinfortier/c3ddb-cluster/linux/c3ddb-key':")
    child.sendline(SLURM_PASSWORD)
    child.expect(" from c3ddb01.cm.cluster")



child.sendline("cd bin/NanoPypes")
time.sleep(5)
cmd = "git pull origin {}".format(branch)
child.sendline(cmd)
c = child.expect("'/home/kf78w/.ssh/id_rsa':")
time.sleep(2)
child.sendline(SSH_PASSWORD)
c = child.expect("From github.com:kforti/NanoPypes")
print("Clone output: ", c)
time.sleep(5)
print('done')
