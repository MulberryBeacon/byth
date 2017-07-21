# -*- coding: utf-8 -*-
"""
Setup module.
"""

# Module import
# --------------------------------------------------------------------------------------------------
from setuptools import setup, find_packages

# Setup
# --------------------------------------------------------------------------------------------------
setup(
    name='byth',
    version='0.0.1',
    description='Small message broker that uses the storm.py library to interact with ActiveMQ.',
    author='Eduardo Ferreira',
    author_email='mulberry.beacon@gmail.com',
    packages=find_packages(),
    install_requires=[
        'stomp.py>=4.1.17'
    ]
)
