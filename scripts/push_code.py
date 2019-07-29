import subprocess
import argparse
import os
import time

import pexpect
import dotenv

dotenv.load_dotenv("env/.env")
PASSWORD = os.environ['LSF_PASSWORD']
SSH_PASSWORD = os.environ['SSH_PASSWORD']


parser = argparse.ArgumentParser(description='Push code to cluster.')
parser.add_argument("-m")
parser.add_argument("-b")
args = parser.parse_args()
msg = args.m
branch = args.b

subprocess.call(["git", "add", "--all"])
subprocess.call(["git", "commit", "-m", msg])
subprocess.call(["git", "push", "origin", branch])

child = pexpect.spawn("ssh kf78w@ghpcc06.umassrc.org")
r = child.expect("password:")

child.sendline(PASSWORD)
child.expect("git 2.9.5 is located under")
child.sendline("cd bin/NanoPypes")
time.sleep(5)
cmd = "git pull origin {}".format(branch)
child.sendline(cmd)
c = child.expect("'/home/kf78w/.ssh/id_rsa':")
time.sleep(2)
child.sendline(SSH_PASSWORD)
c = child.expect("From github.com:kforti/NanoPypes")
time.sleep(5)
print('done')
