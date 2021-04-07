import os
from shutil import copyfile
import yaml
import click
from jinja2 import Template

from notebook_pge_wrapper.spec_generator import generate_spec_files
from notebook_pge_wrapper.execute_notebook import execute as execute_notebook


__SETTINGS = 'settings.yml'
__NOTEBOOK_DIR = 'notebook_pges'
__DOCKER_DIR = 'docker'
__DOCKERFILE_TEMPLATE = 'Dockerfile.template'
__DOCKERFILE = 'Dockerfile'
__README_FILE = 'README.md'


def read_settings(f):
    """
    reads the settings.yaml file
    :param f: file path to settings.yml
    :return: Dict[str, str]
    """
    try:
        with open(f, 'r') as f:
            settings = yaml.safe_load(f)
            return settings
    except FileNotFoundError as e:
        raise e
    except yaml.YAMLError as e:
        raise e
    except Exception as e:
        raise e


def read_docker_template(f):
    """
    reads docker template file
    :param f:
    :return: str
    """
    with open(f, 'r') as f:
        return f.read()


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
    └── notebook_pges/

    :param project: New notebook project name (or path)
    """
    if not project:
        raise RuntimeError("project must be supplied, ie. notebook-pge-wrapper create <project_root>")

    project_root = os.path.dirname(os.path.abspath(__file__))

    docker_directory = os.path.join(project, __DOCKER_DIR)
    notebook_pges_directory = os.path.join(project, __NOTEBOOK_DIR)

    templates = os.path.join(project_root, '..', 'templates')
    readme_file = os.path.join(templates, __README_FILE)

    if not os.path.exists(project):
        os.mkdir(project)

    # create docker directory
    if not os.path.exists(docker_directory):
        os.mkdir(docker_directory)

    settings = read_settings(os.path.join(templates, __SETTINGS))
    base_image = settings['base_image']

    docker_template = read_docker_template(os.path.join(templates, __DOCKERFILE_TEMPLATE))
    docker_template = Template(docker_template)
    docker_template = docker_template.render(base_image=base_image, project=project)

    # create Dockerfile
    with open(os.path.join(docker_directory, __DOCKERFILE), 'w') as f:
        f.write(docker_template)

    # copy Dockerfile.template to project
    copyfile(
        os.path.join(templates, __DOCKERFILE_TEMPLATE),
        os.path.join(project, __DOCKER_DIR, __DOCKERFILE_TEMPLATE)
    )

    # create notebook_pges directory
    if not os.path.exists(notebook_pges_directory):
        os.mkdir(notebook_pges_directory)

    # create README.md
    copyfile(readme_file, os.path.join(project, __README_FILE))

    # copy settings file
    copyfile(
        os.path.join(templates, __SETTINGS),
        os.path.join(project, __SETTINGS)
    )


@cli.command()
@click.argument('update')
def docker(update):
    """
    updates the Dockerfile template with values from settings.yml
    :param update:
    """
    base, project_root = os.path.split(os.getcwd())

    settings = read_settings(__SETTINGS)
    base_image = settings['base_image']

    docker_template = read_docker_template(os.path.join(__DOCKER_DIR, __DOCKERFILE_TEMPLATE))
    docker_template = Template(docker_template)
    docker_template = docker_template.render(base_image=base_image, project=project_root)

    # updating Dockerfile
    with open(os.path.join(__DOCKER_DIR, __DOCKERFILE), 'w') as f:
        f.write(docker_template)


@cli.command()
@click.argument('notebook_path')
def specs(notebook_path):
    """
    Generates the hysdsio and job specs for json files (in the docker directory) for a notebook \n
    enter "all" to generate all spec files in notebook_pges/ \n
    ie. notebook-pge-wrapper specs <notebook_path or all>

    :param notebook_path: path to the .ipynb file
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


@cli.command()
@click.argument('notebook_path')
@click.option('--context', 'context')
def execute(notebook_path, context=None):
    """
    Execute a .ipynb notebook
    :param notebook_path: path to the .ipynb file
    :param context: path to the _context.json file, default to _context.json in current directory if not supplied
    """
    if not notebook_path.endswith('.ipynb'):
        raise RuntimeError('%s is not a .ipynb file' % notebook_path)

    if context is None:
        context = '_context.json'
    execute_notebook(notebook_path, ctx_file=context)
