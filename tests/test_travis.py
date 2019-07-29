import pytest
import subprocess
import argparse
import os
import time

import pexpect



def test_travis():
    assert True

def test_lsf_build():

    PASSWORD = os.environ['LSF_PASSWORD']

    child = pexpect.spawn("ssh kf78w@ghpcc06.umassrc.org")
    r = child.expect("password:")

    child.sendline(PASSWORD)
    child.expect("git 2.9.5 is located under")
    l = child.sendline("ls")
    time.sleep(5)
    print(l)

if __name__ == '__main__':
    test_travis()
    test_lsf_build()
