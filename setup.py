from setuptools import setup, find_packages

def do_setup():
    setup(
        name='notebook_pge_wrapper',
        version='1.0.3',
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
            'Jinja2>=2.11.3',
            'PyYAML>=5.4.1',
            'papermill>=2.2.0',
        ],
        package_data={
            'notebook_pge_wrapper' : [
                'templates/Dockerfile.template',
                'templates/*.ipynb',
                'templates/settings.yml',
                'templates/README.md',
             ],
        },
    )

if __name__ == "__main__":
    do_setup()
