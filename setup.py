#!/usr/bin/env python

from setuptools import setup
from waspmoteFrameParser import __version__ as version

setup(
    name="waspmoteFrameParser",
    version=version,
    author="Ferdinand Koeppen",
    autohr_email="fkoeppen@edu.aau.at",
    description="Frame parser for waspmote frames",
    url="https://github.com/TheElk205/waspmoteFrameParser",
    license="MIT",
    packages=["waspmoteFrameParser"]
)
