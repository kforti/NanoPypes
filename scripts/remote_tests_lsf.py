import subprocess
import argparse
import os
import time

import pexpect
import dotenv



dotenv.load_dotenv("env/.env")
PASSWORD = os.environ['PASSWORD']

#parser = argparse.ArgumentParser(description='Push code to cluster.')
#parser.add_argument("-m")
#args = parser.parse_args()

child = pexpect.spawn("ssh kf78w@ghpcc06.umassrc.org")
r = child.expect("password:")

child.sendline(PASSWORD)
child.expect("git 2.9.5 is located under")
child.sendline("cd bin/NanoPypes")
time.sleep(5)
response = child.sendline("python3 tests/test_cluster.py")
print(response)
