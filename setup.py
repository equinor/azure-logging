# Always prefer setuptools over distutils
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = "Readme: https://github.com/equinor/azure-logging"

setup(
    name='azure-logging',


    version='1.0.0',

    description='Azure logging',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/equinor/azure-logging',

    # Author details
    author='Mats Grønning Andersen',
    author_email='mgand@equinor.com',

    # Choose your license
    license='MIT',

    py_modules=['azure_logging'],
    # download_url="https://github.com/equinor/azure-logging",
)
