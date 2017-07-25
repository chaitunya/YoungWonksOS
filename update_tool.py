#!/usr/bin/env python3
# Copyright WONKSKNOW LLC

from wheel.install import WheelFile
from pydoc import ModuleScanner
import pip
import pprint
import os
import sys
from pkg_resources import parse_version, get_distribution
import argparse
import requests
import warnings


DL_LIST_URL = "https://drive.google.com/uc?export=download&id=0B-UtaVJD_Il0bmVmTm9mMjRBeDg"
DEBUG = True
INIT_STR_LEN = 9


def get_modules():
    """Returns list of modules that are available to import"""
    modules = []
    def module_scanner_callback(path, modname, desc, modules=modules):
        if modname and modname[-INIT_STR_LEN:] == ".__init__":
            modname = modname[:-INIT_STR_LEN] + " (package)"
        # Checks if the module is top-level (if there is no dot)
        if modname.find(".") < 0:
            modules.append(modname)

    def onerror(modname):
        module_scanner_callback(None, modname, None)
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        try:
            ModuleScanner().run(module_scanner_callback, onerror=onerror)
        except Warning as w:
            if debug:
                with open("install.log", "w+") as install_log:
                    install_log.write(w)
    return modules

def check_install(module, current_version=None, debug=False):
    """Checks if module is installed.
    If version is not None, then it checks if the version for the module is at least version"""
    modules = get_modules()
    if module in modules:
        module_version = get_distribution(module).version
        if current_version is not None:
            if parse_version(current_version) <= parse_version(module_version):
                return True
            else:
                return False
        else:
            return True
    return False

def install_module(mod_name, mod_vals, debug=False):
    already_installed = check_install(mod_vals["ImportedName"], mod_vals["Version"])
    if not already_installed:
        print("Installing module %s version %s" % (mod_name, mod_vals["Version"]))
        for dep in mod_vals["Dependencies"]:
            if not check_install(dep):
                if debug:
                    print("Did not install module; did not have all dependencies. Hopefully, this module will be placed on the waitlist")
                return False
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

    return 0

if __name__ == "__main__":
    exit(main(True))

