from sys import version, exit
from setuptools import setup

requirements = open("requirements.txt").read().split()

setup(
    name = 'bagcat',
    version = '0.0.2',
    url = 'https://github.com/umd-mith/bagcat/',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['bagcat',],
    scripts = ['scripts/bagcat'],
    install_requires = requirements,
    description = "A command line utility for managing BagIt packages in Amazon S3")
