#!/usr/bin/env python
import os
from setuptools import setup

def read(filen):
    with open(os.path.join(os.path.dirname(__file__), filen), "r") as fp:
        return fp.read()
 
setup (
    name = "glance",
    version = "0.1",
    description="Servers, at a glance",
    long_description=read("README.md"),
    author="Alec Elton",
    author_email="alec.elton@gmail.com", # Removed to limit spam harvesting.
    url="",
    packages=["glance"],
    install_requires=[],
)