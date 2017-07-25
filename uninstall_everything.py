#!/usr/bin/env python3
"""
This script is meant for debugging purposes. It quickly uninstalls the python packages installed by YW_update_tool.py or YW_install_tool.py
"""
import pip

libs = ["numpy", "scipy", "cython"]

def main():
    for lib in libs:
        try:
            pip.main(["uninstall", lib])
        except Exception as e:
            print(e)

