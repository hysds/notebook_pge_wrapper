import os
from shutil import copyfile
from pathlib import Path

from notebook_pge_wrapper.spec_generator import generate_job_spec, generate_hysdsio, extract_hysds_specs
from .execute_notebook import execute


__SETTINGS_DIR = os.path.join(str(Path.home()), '.config/notebook-pge-wrapper')


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
