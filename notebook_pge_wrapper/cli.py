import os
from shutil import copyfile
import click

from notebook_pge_wrapper.spec_generator import generate_spec_files
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
    Creates the project root directory:\n
    <project_root>\n
    ├── README.md\n
    ├── docker/\n
    │   └── Dockerfile\n
    └── notebook_pges/\n

    :param project: str: CLI argument
    :return: None
    """
    if not project:
        raise RuntimeError("project must be supplied, ie. notebook-pge-wrapper create <project_root>")

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
@click.argument('notebook_path')
def specs(notebook_path):
    """
    Generates the hysdsio and job specs for json files (in the docker directory) for a notebook \n
    enter "all" to generate all spec files in notebook_pges/ \n
    ie. notebook-pge-wrapper specs <notebook_path or all>

    :param notebook_path: str
    :return: None
    """
    if notebook_path == "all":
        for nb in os.listdir('notebook_pges'):  # iterate through notebook_pges/ directory
            if not nb.endswith('.ipynb'):
                print('%s is not a notebook, skipping...' % nb)
                continue
            print('inspecting notebook: %s' % nb)
            generate_spec_files(nb)
    else:
        if not os.path.isfile(notebook_path):
            raise RuntimeError("notebook %s not found" % notebook_path)

        nb = notebook_path.split('/')
        nb = nb[1]
        print('inspecting notebook: %s' % nb)
        generate_spec_files(nb)
