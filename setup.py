from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

from setuptools import setup, find_packages

setup(
    name='notebook_pge_wrapper',
    version='1.0.0',
    long_description='Library to generate hysds_io and job_specs for Jupyter notebooks',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'future>=0.17.1',
        'papermill>=2.2.0',
    ]
)