from sys import version, exit
from setuptools import setup

requirements = open("requirements.txt").read().split()

with open("README.md") as f:
    long_description = f.read()

setup(
    name = 'bagcat',
    version = '0.0.6',
    url = 'https://github.com/umd-mith/bagcat/',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['bagcat',],
    install_requires = requirements,
    description = "A command line utility for managing BagIt packages in Amazon S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["bagcat=bagcat:main"]},
)
