# Copyright WONKSKNOW LLC

"""
Install script for the update_tool.py
This just installs a few packages, runs the update_tool.py,
then installs the update_tool.py script to /usr/local/bin/yw_update_tool
"""

import pip
import subprocess as sp
import runpy
import os
import sys

try:
    import requests
except:
    try:
        pip.main(["requests"])
    except SystemExit:
        pass
    import requests

PROJECT_URL="https://bitbucket.org/chaitunya/YoungWonksOS.git"
TMP_LOCATION = "/tmp/YoungWonksOS"
def clone(repo_ur):
    cmd = ["git", "clone", repo_url, TMP_LOCATION]
    p = sp.Popen(cmd)
    p.wait()

clone(PROJECT_URL)
sys.argv = ["install"]
runpy.run_path(os.path.join(TMP_LOCATION), "setup.py"), run_name="__main__")
