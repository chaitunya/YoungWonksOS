#!/usr/bin/env python3
# Copyright WONKSKNOW LLC
__version__ = "1.0.3"

from wheel.install import WheelFile
from pydoc import ModuleScanner
import pip
import pprint
import os
import sys
import shlex
from pkg_resources import parse_version
import argparse
import requests
import warnings
import subprocess as sp


DL_LIST_URL = "https://pastebin.com/raw/R8AURQC5"
INIT_STR_LEN = 9

def check_install(module, at_least_version=None, debug=False):
    """Checks if module is installed.
    If version is not None, then it checks if the version for the module is at least version"""
    try:
        module_version = __import__(module).__version__
        is_module = True
    except ImportError as e:
        is_module = False
    if is_module:
        if at_least_version is not None:
            if parse_version(at_least_version) <= parse_version(module_version):
                return True
            else:
                return False
        else:
            return True
    else:
        False

def install_module(mod_name, mod_vals, debug=False):
    """Checks for dependencies, then installs module"""
    already_installed = check_install(mod_vals["ImportedName"], mod_vals["Version"])
    if not already_installed:
        for dep in mod_vals["Dependencies"]:
            if not check_install(dep):
                if debug:
                    print("Did not install module; did not have all dependencies. Hopefully, this module will be placed on the waitlist")
                return False
        print("Installing module %s version %s" % (mod_name, mod_vals["Version"]))
        print("Downloading module")
        install_req = requests.get(mod_vals["DownloadLink"])
        install_filename = os.path.join("/tmp", mod_vals["Filename"])
        install_content = install_req.content
        with open(install_filename, "wb") as mod_file:
            mod_file.write(install_content)
        print("Installing module")
        wheelfile = WheelFile(install_filename)
        try:
            wheelfile.install(force=True)
        except ValueError as e:
            print(e)
        installed = check_install(mod_vals["ImportedName"], mod_vals["Version"])
        os.remove(install_filename)
        if installed:
            print("Successfully installed")
        else:
            print("Failed to install")
        return installed
    else:
        if debug:
            print("Not installing module. It is %s that this module was already installed" % already_installed)
        return already_installed

def main(debug=False):
    dl_list_request = requests.get(DL_LIST_URL)
    dl_list = dl_list_request.json()
    run_commands = dl_list.pop("RunCommands")
    waitlist = []
    if debug:
        pprint.pprint(dl_list)

    for module, values in dl_list.items():
        installed = install_module(module, values, debug)
        if not installed:
            waitlist.append([module, values])
        if debug:
            print("%s: %s" % (module, values))

    if debug:
        pprint.pprint(waitlist)

    for module, values in waitlist:
        installed = install_module(module, values, debug)
        if debug:
            print("%s: %s" % (module, values))
    for command in run_commands:
       p = sp.Popen(shlex.split(command))
       p.wait()

    return 0

if __name__ == "__main__":
    exit(main())

