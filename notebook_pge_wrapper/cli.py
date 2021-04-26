import os
from pathlib import Path
from shutil import copyfile
import yaml
import click
from jinja2 import Template

from notebook_pge_wrapper.spec_generator import generate_spec_files
from notebook_pge_wrapper.execute_notebook import execute as execute_notebook


__SETTINGS = 'settings.yml'
__SETTINGS_DIR = os.path.join(str(Path.home()), '.config/notebook-pge-wrapper')
__SETTINGS_LOC = os.path.join(__SETTINGS_DIR, __SETTINGS)

__NOTEBOOK_DIR = 'notebook_pges'
__DOCKER_DIR = 'docker'
__DOCKERFILE_TEMPLATE = 'Dockerfile.template'
__DOCKERFILE = 'Dockerfile'
__README_FILE = 'README.md'

__REQUIREMENTS = 'requirements.ipynb'

__PGE_CREATE_NOTEBOOK_FILE = 'pge_create.ipynb'
__SUBMIT_JOB_NOTEBOOK_FILE = 'submit_job.ipynb'
__SAMPLE_PGE_NOTEBOOK_FILE = 'sample_pge.ipynb'
__PELE_SETUP_NOTEBOOK_FILE = 'pele_setup.ipynb'

__SETTINGS_DESCRIPTION = "(optional) path to settings.yml, will default to " \
                         "~/.config/notebook-pge-wrapper/settings.yml if not supplied"


def settings_check():
    if not os.path.exists(__SETTINGS_DIR):
        print('%s not found, creating directory..' % __SETTINGS_DIR)
        os.makedirs(__SETTINGS_DIR)

    if not Path(os.path.join(__SETTINGS_DIR, 'settings.yml')).is_file():
        print('settings.yml not found, copying from library template (please revise)')
        package_root = os.path.dirname(os.path.abspath(__file__))
        copyfile(
            os.path.join(package_root, '..', 'templates', 'settings.yml'),
            os.path.join(__SETTINGS_DIR, 'settings.yml')
        )


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
    :param f: file path to Dockerfile.template
    :return: str
    """
    with open(f, 'r') as f:
        return f.read()


@click.group()
def cli():
    """A CLI wrapper for notebook_pge_wrapper"""


@cli.command()
@click.argument('project')
@click.option('--settings', '-s', default=None, help=__SETTINGS_DESCRIPTION)
def create(project, settings=None):
    """
    Creates the project root directory:\n
    <project_root>\n
    ├── README.md\n
    ├── docker/\n
    │   └── Dockerfile\n
    ├── pge_create.ipynb/\n
    ├── submit_job.ipynb/\n
    ├── pele_setup.ipynb/\n
    └── notebook_pges/\n
        └── sample_pge.ipynb
    """
    if not project:
        raise RuntimeError("project must be supplied, ie. notebook-pge-wrapper create <project_root>")

    project_root = os.path.dirname(os.path.abspath(__file__))

    docker_directory = os.path.join(project, __DOCKER_DIR)
    notebook_pges_directory = os.path.join(project, __NOTEBOOK_DIR)

    templates = os.path.join(project_root, '..', 'templates')
    readme_file = os.path.join(templates, __README_FILE)
    pge_create_notebook_file = os.path.join(templates, __PGE_CREATE_NOTEBOOK_FILE)
    submit_job_notebook_file = os.path.join(templates, __SUBMIT_JOB_NOTEBOOK_FILE)
    sample_pge_notebook_file = os.path.join(templates, __SAMPLE_PGE_NOTEBOOK_FILE)
    pele_setup_notebook_file = os.path.join(templates, __PELE_SETUP_NOTEBOOK_FILE)

    if settings is None:
        settings_check()
        settings_data = read_settings(__SETTINGS_LOC)
    else:
        settings_data = read_settings(settings)

    if not os.path.exists(project):
        os.mkdir(project)

    # create docker directory
    if not os.path.exists(docker_directory):
        os.mkdir(docker_directory)

    base_image = settings_data['base_image']
    user = settings_data['user']

    docker_template = read_docker_template(os.path.join(templates, __DOCKERFILE_TEMPLATE))
    docker_template = Template(docker_template)
    docker_template = docker_template.render(base_image=base_image, user=user, project=project)

    # create Dockerfile
    with open(os.path.join(docker_directory, __DOCKERFILE), 'w') as f:
        f.write(docker_template)

    # copy Dockerfile.template to project
    copyfile(
        os.path.join(templates, __DOCKERFILE_TEMPLATE),
        os.path.join(project, __DOCKERFILE_TEMPLATE)
    )

    # copy requirements.ipynb to project
    copyfile(
        os.path.join(templates, __REQUIREMENTS),
        os.path.join(project, __DOCKER_DIR, __REQUIREMENTS)
    )

    # create notebook_pges directory
    if not os.path.exists(notebook_pges_directory):
        os.mkdir(notebook_pges_directory)

    # create pge_create notebook
    pge_create_notebook_dest = os.path.join(project, __PGE_CREATE_NOTEBOOK_FILE)
    with open(pge_create_notebook_file, 'r') as fin, \
            open(pge_create_notebook_dest, 'w+') as fout:
        templated_pge_create_content = fin.read().replace('PGE_NAME_PLACEHOLDER', project)
        fout.write(templated_pge_create_content)

    # create submit_job notebook
    submit_job_notebook_dest = os.path.join(project, __SUBMIT_JOB_NOTEBOOK_FILE)
    with open(submit_job_notebook_file, 'r') as fin, \
            open(submit_job_notebook_dest, 'w+') as fout:
        templated_submit_job_content = fin.read().replace('PGE_NAME_PLACEHOLDER', project)
        fout.write(templated_submit_job_content)

    # create pele_setup notebook
    copyfile(pele_setup_notebook_file, os.path.join(project, __PELE_SETUP_NOTEBOOK_FILE))
        
    # create sample pge notebook
    copyfile(sample_pge_notebook_file, os.path.join(notebook_pges_directory, f'{project}_{__SAMPLE_PGE_NOTEBOOK_FILE}'))

    # create README.md
    copyfile(readme_file, os.path.join(project, __README_FILE))


@cli.command()
@click.option('--settings', '-s', default=None, help=__SETTINGS_DESCRIPTION)
def dockerfile(settings=None):
    """
    updates the Dockerfile template with values from settings.yml
    """
    base, project_root = os.path.split(os.getcwd())

    if settings is None:
        settings_check()
        settings_data = read_settings(__SETTINGS_LOC)
    else:
        settings_data = read_settings(settings)
    base_image = settings_data['base_image']
    user = settings_data['user']

    docker_template = read_docker_template(__DOCKERFILE_TEMPLATE)
    docker_template = Template(docker_template)
    docker_template = docker_template.render(base_image=base_image, user=user, project=project_root)

    # updating Dockerfile
    with open(os.path.join(__DOCKER_DIR, __DOCKERFILE), 'w') as f:
        f.write(docker_template)


@cli.command()
@click.argument('notebook_path')
@click.option('--settings', '-s', default=None, help=__SETTINGS_DESCRIPTION)
def specs(notebook_path, settings=None):
    """
    Generates the hysdsio and job specs for json files (in the docker directory) for a notebook \n
    enter "all" to generate all spec files in notebook_pges/ \n
    ie. notebook-pge-wrapper specs <notebook_path or all>
    """
    if settings is None:
        settings_check()
        settings_data = read_settings(__SETTINGS_LOC)
    else:
        settings_data = read_settings(settings)
    user = settings_data['user']

    if notebook_path == "all":
        for nb in os.listdir('notebook_pges'):  # iterate through notebook_pges/ directory
            if not nb.endswith('.ipynb'):
                print('%s is not a notebook, skipping...' % nb)
                continue
            print('inspecting notebook: %s' % nb)
            generate_spec_files(nb, user)
    else:
        if not os.path.isfile(notebook_path):
            raise RuntimeError("notebook %s not found" % notebook_path)

        nb = notebook_path.split('/')
        nb = nb[1]
        print('inspecting notebook: %s' % nb)
        generate_spec_files(nb, user)


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
