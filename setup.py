#!/usr/bin/env python3
from src.update_tool import __version__
from setuptools import setup, find_packages
from os import path
import time

current_dir = path.abspath(path.dirname(__file__))
long_description = """
This is a tool made for YoungWonks students. This tool installs and updates several packages: OpenCV, NumPy, SciPy, and Cython. There will be more packages added in the future. This tool doesn't require you to compile these packages, as this takes a long time. We don't want you to spend time creating your programming environment; we want you to spend time *using* your programming environment. NOTE: THIS IS SPECIFICALLY MEANT FOR THE RASPBERRY PI OR OTHER LINUX ARM v7 SYSTEMS.
"""
print(__import__("sys").argv)
setup(
    name="YoungWonks Update Tool",
    version=__version__,
    description="Tool that updates some packages for YoungWonks students",
    long_description=long_description,
    url="http://youngwonks.com",
    author="Chaitanya Nookala",
    author_email="chaitanya.nookala@gmail.com",

    license="MIT",
    classifiers=[
        "Development Status :: 5",

        "Intended Audience :: YoungWonks Students",

        "Topic :: Software Development :: Build Tools",

        "License :: :: MIT",

        "Programming Language :: Python :: 3",

    ],

    keywords="",
    py_modules=["update_tool"],
    package_dir={"": "src"},
    install_requires=["requests"],
    extras_require={},
    scripts=["bin/update_YW"],
)
