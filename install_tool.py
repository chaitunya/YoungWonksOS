#!/usr/bin/env python3
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
import shutil

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
def clone(repo_url):
    cmd = ["git", "clone", repo_url, TMP_LOCATION]
    p = sp.Popen(cmd)
    p.wait()

clone(PROJECT_URL)
setup_path = os.path.join(TMP_LOCATION, "setup.py")
sys.argv = [setup_path, "install"]
runpy.run_path(setup_path, run_name="__main__")
shutil.rmtree(TMP_LOCATION)
