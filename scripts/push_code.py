import subprocess
import argparse
import os

import pexpect

parser = argparse.ArgumentParser(description='Push code to cluster.')
parser.add_argument("-m")
parser.add_argument("-b")
args = parser.parse_args()
msg = args.m
branch = args.b



subprocess.call(["git", "--add", "all"])
subprocess.call(["git", "commit", "-m", msg])
subprocess.call(["git", "push", "origin", branch])

psw_prompt = "kf78w@ghpcc06.umassrc.org's password:"

child = pexpect.spawn("ssh kf78w@ghpcc06.umassrc.org")
child.sendline(os.environ['PASSWORD'])
child.expect("This is the University of Massachusetts information technology environment.")
child.sendline("bin/NanoPypes")
child.sendline("git pull origin {}".format(branch))

