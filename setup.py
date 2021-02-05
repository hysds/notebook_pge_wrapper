from setuptools import setup, find_packages

setup(
    name='notebook_pge_wrapper',
    version='1.0.1',
    long_description='Library to generate hysds_io and job_specs for Jupyter notebooks',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'notebook-pge-wrapper = notebook_pge_wrapper.cli:cli'
        ]
    },
    install_requires=[
        'click>=7.1.2',
        'papermill>=2.2.0',
    ]
)
