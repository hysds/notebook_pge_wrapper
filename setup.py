from setuptools import setup, find_packages

setup(
    name='notebook_pge_wrapper',
    version='1.0.0',
    long_description='Library to generate hysds_io and job_specs for Jupyter notebooks',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'papermill>=2.2.0',
    ]
)