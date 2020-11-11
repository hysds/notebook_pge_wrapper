import os
from shutil import copyfile
import click

import json

from notebook_pge_wrapper.spec_generator import generate_job_spec, generate_hysdsio, extract_hysds_specs
# from notebook_pge_wrapper.execute_notebook import execute


__NOTEBOOK_DIR = 'notebook_pges'
__DOCKER_DIR = 'docker'
__DOCKERFILE = 'Dockerfile'
__README_FILE = 'README.md'


@click.group()
def cli():
    """A CLI wrapper for notebook_pge_wrapper"""


@cli.command()
@click.argument('project')
def create(project):
    """
    Creates the project root directory:
    $ notebook-pge-wrapper create <project_root>
    <project_root>
    ├── README.md
    ├── docker/
    │   └── Dockerfile
    └── notebook_pges/

    :param project: str: CLI argument
    :return: None
    """
    project_root = os.path.dirname(os.path.abspath(__file__))

    docker_directory = os.path.join(project, __DOCKER_DIR)
    notebook_pges_directory = os.path.join(project, __NOTEBOOK_DIR)

    templates = os.path.join(project_root, '..', 'templates')
    docker_file = os.path.join(templates, __DOCKERFILE)
    readme_file = os.path.join(templates, __README_FILE)

    if not os.path.exists(project):
        os.mkdir(project)

    # create docker directory
    if not os.path.exists(docker_directory):
        os.mkdir(docker_directory)

    # create Dockerfile
    copyfile(docker_file, os.path.join(docker_directory, __DOCKERFILE))

    # create notebook_pges directory
    if not os.path.exists(notebook_pges_directory):
        os.mkdir(notebook_pges_directory)

    # create README.md
    copyfile(readme_file, os.path.join(project, __README_FILE))


@cli.command()
@click.option('--notebook', '-n', 'notebook_path', help='number of greetings')
def specs(notebook_path):
    """
    Generates the hysdsio and job specs for json files (saved in the docker directory) for a notebook
    :param notebook_path: str
    :return: None
    """
    if notebook_path is None:
        raise RuntimeError("notebook argument (--notebook or -n) must be supplied")

    if not os.path.isfile(notebook_path):
        raise RuntimeError("notebook %s not found" % notebook_path)

    notebook = notebook_path.split('/')
    notebook = notebook[1]

    nb_split = notebook.split('.')
    root_name = nb_split[0]

    hysds_specs = extract_hysds_specs(notebook_path)
    time_limit = hysds_specs.get('time_limit')
    soft_time_limit = hysds_specs.get('soft_time_limit')
    disk_usage = hysds_specs.get('disk_usage')
    submission_type = hysds_specs.get('submission_type', 'individual')
    required_queue = hysds_specs.get('required_queue', 'factotum-job_worker-small')
    label = hysds_specs.get('label')

    # generate hysds_io
    hysdsio = generate_hysdsio(nb_name=notebook_path, sub_type=submission_type, job_label=label)
    hysdsio_file = 'hysds-io.json.%s' % root_name
    hysdsio_file_location = os.path.join('docker', hysdsio_file)

    with open(hysdsio_file_location, 'w+') as f:
        json.dump(hysdsio, f, indent=2)
    print('generated %s' % hysdsio_file_location)

    job_spec = generate_job_spec(nb_name=notebook_path, soft_time_limit=soft_time_limit, time_limit=time_limit,
                                 required_queue=required_queue, disk_usage=disk_usage)
    job_spec_file = 'job-spec.json.%s' % root_name
    job_spec_file_location = os.path.join('docker', job_spec_file)

    with open(job_spec_file_location, 'w+') as f:
        json.dump(job_spec, f, indent=2)
    print('generated %s' % job_spec_file_location)


