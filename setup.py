#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    install_requires=[
        'sqlalchemy==1.1.11',
        'requests==2.18.1',
        'Flask==0.12.2',
        'voluptuous==0.10.5'
    ],
)
